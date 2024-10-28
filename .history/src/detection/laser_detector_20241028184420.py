# src/detection/laser_detector.py

import cv2
import numpy as np
from config import DISTANCE_CALIBRATION, MIN_CONTOUR_AREA
from utils.image_processing import get_red_mask, apply_blur

def estimate_distance(area):
    if area == 0:
        return None
    return DISTANCE_CALIBRATION / np.sqrt(area)

def is_circle_like(contour):
    # Calculate contour area and perimeter
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    # Avoid division by zero
    if perimeter == 0:
        return False
    # Calculate circularity
    circularity = 4 * np.pi * (area / (perimeter * perimeter))
    # A circularity close to 1 indicates a circle
    return 0.7 < circularity < 1.3

def detect_laser_pointer(frame):
    # Convert to HSV and apply red color mask
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = get_red_mask(hsv)
    mask = apply_blur(mask)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None, None

    # Largest contour by area, assumed to be the laser spot
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)

    # Filter based on area, brightness, and shape
    if area < MIN_CONTOUR_AREA or area > 300:  # Filter based on size
        return None, None, None

    # Check if the contour is circle-like to avoid detecting ears or lips
    if not is_circle_like(largest_contour):
        return None, None, None

    # Get bounding rectangle for the laser spot
    x, y, w, h = cv2.boundingRect(largest_contour)
    distance = estimate_distance(area)
    return (x, y, w, h), distance, area
