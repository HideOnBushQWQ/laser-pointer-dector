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
        
        # Define a refined red color range for bright center detection
        lower_red_center = np.array([0, 120, 120])
        upper_red_center = np.array([10, 255, 255])
        center_mask = cv2.inRange(hsv, lower_red_center, upper_red_center)
        
        # Detect contours in the center mask
        center_contours, _ = cv2.findContours(center_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in center_contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            
            # Directly check area and proceed with drawing
            if area > self.area_threshold:
                print(f"Drawing Rectangle - Position: {(x, y, w, h)}, Area: {area}")
                
                # Draw a green rectangle around the detected laser pointer region
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Estimate the distance to the laser
                distance = self.estimate_distance(w)
                
                # Annotate the distance on the frame
                cv2.putText(frame, f"Distance: {distance:.2f} m", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Display the frame to confirm rectangle is drawn
        cv2.imshow("Laser Detection", frame)
        cv2.waitKey(1)  # Required to update the frame display
        
        return frame

    def estimate_distance(self, pixel_width):
        """Estimate the distance to the laser based on its pixel width."""
        focal_length = CAMERA_PARAMS["focal_length"]
        real_laser_diameter = CAMERA_PARAMS["real_laser_diameter"]
        distance = (real_laser_diameter * focal_length) / pixel_width
        return distance
