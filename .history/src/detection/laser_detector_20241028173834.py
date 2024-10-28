# src/detection/laser_detector.py

import cv2
import numpy as np
from utils.image_processing import apply_erosion, apply_dilation
from config import CAMERA_PARAMS

class LaserDetector:
    def __init__(self, thresholds):
        self.brightness_threshold = thresholds["brightness_threshold"]
        self.red_intensity_threshold = thresholds["red_intensity_threshold"]
        self.area_threshold = thresholds["area_threshold"]
    
    def detect_laser(self, frame):
        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define red color range and create a mask
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Apply erosion and dilation to reduce noise
        mask = apply_erosion(mask, iterations=2)
        mask = apply_dilation(mask, iterations=2)
        
        # Find contours in the red mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Check if the contour area is above the threshold
            if cv2.contourArea(contour) > self.area_threshold:
                # Calculate the bounding box for the contour
                x, y, w, h = cv2.boundingRect(contour)
                roi = frame[y:y+h, x:x+w]

                # Check the brightness at the center of the region
                center_brightness = np.mean(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY))
                
                if center_brightness >= self.brightness_threshold:
                    # This is the laser pointer region
                    # Draw a green rectangle around it
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Estimate the distance to the laser
                    distance = self.estimate_distance(w)
                    
                    # Annotate the distance on the frame
                    cv2.putText(frame, f"Distance: {distance:.2f} m", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame

    def estimate_distance(self, pixel_width):
        """Estimate the distance to the laser based on its pixel width."""
        focal_length = CAMERA_PARAMS["focal_length"]
        real_laser_diameter = CAMERA_PARAMS["real_laser_diameter"]
        distance = (real_laser_diameter * focal_length) / pixel_width
        return distance
