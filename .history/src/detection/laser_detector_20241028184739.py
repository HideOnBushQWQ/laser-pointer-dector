# src/detection/laser_detector.py

import cv2
import numpy as np
from config import DISTANCE_CALIBRATION, MIN_CONTOUR_AREA, BRIGHTNESS_THRESHOLD
from utils.image_processing import get_red_mask, apply_blur

def estimate_distance(area):
    if area == 0:
        return None
    return DISTANCE_CALIBRATION / np.sqrt(area)

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

    if area < MIN_CONTOUR_AREA:
        return None, None, None

    # Calculate average brightness within the contour
    mask_contour = np.zeros_like(mask)
    cv2.drawContours(mask_contour, [largest_contour], -1, 255, thickness=cv2.FILLED)
    mean_val = cv2.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), mask=mask_contour)[0]

    # Check if the brightness is above the threshold
    if mean_val < BRIGHTNESS_THRESHOLD:
        return None, None, None

    # Get bounding rectangle for the laser spot
    x, y, w, h = cv2.boundingRect(largest_contour)
    distance = estimate_distance(area)
    return (x, y, w, h), distance, area