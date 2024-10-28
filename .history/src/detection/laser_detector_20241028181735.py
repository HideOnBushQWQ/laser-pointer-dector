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
            
            # Step 1: Check if the area is above threshold and brightness is high
            if area > self.area_threshold:
                roi_center = frame[y:y+h, x:x+w]
                gray_center = cv2.cvtColor(roi_center, cv2.COLOR_BGR2GRAY)
                center_brightness = np.mean(gray_center)
                
                # Calculate red dominance
                mean_red_channel = np.mean(roi_center[:, :, 2])
                mean_green_channel = np.mean(roi_center[:, :, 1])
                mean_blue_channel = np.mean(roi_center[:, :, 0])

                # Debug output for center detection
                print(f"Center Detection - Position: {(x, y, w, h)}, Area: {area}, Brightness: {center_brightness}, "
                      f"Red: {mean_red_channel}, Green: {mean_green_channel}, Blue: {mean_blue_channel}")
                
                # Step 2: Check brightness and red dominance
                if center_brightness >= self.brightness_threshold and \
                   mean_red_channel > mean_green_channel + 50 and \
                   mean_red_channel > mean_blue_channel + 50:
                    # Draw a green rectangle around the detected laser pointer region
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
