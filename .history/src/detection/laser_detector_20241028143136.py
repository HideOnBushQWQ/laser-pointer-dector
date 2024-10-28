# laser_detector.py
import cv2
import numpy as np
from config import CONFIG
from utils.image_processing import apply_dilation, apply_erosion

def detect_laser_point(frame):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define HSV range for bright red
    lower_red = np.array([0, 120, CONFIG["red_threshold"][0]])
    upper_red = np.array([10, 255, CONFIG["red_threshold"][1]])
    
    # Threshold image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # Apply erosion and dilation to reduce noise
    mask = apply_erosion(mask, CONFIG["erosion_iterations"])
    mask = apply_dilation(mask, CONFIG["dilation_iterations"])
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour which should be the laser point
        laser_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(laser_contour)
        cx, cy = x + w // 2, y + h // 2  # Center of the bounding box

        # Calculate distance (simple scaling for demonstration)
        distance = CONFIG["distance_scale_factor"] / (w * h + 1e-5)
        
        return (cx, cy), (x, y, w, h), distance
    return None, None, None
