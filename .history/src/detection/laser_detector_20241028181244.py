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
        
        # Define initial red color range for bright center
        lower_red_center = np.array([0, 150, 150])
        upper_red_center = np.array([10, 255, 255])
        center_mask = cv2.inRange(hsv, lower_red_center, upper_red_center)
        
        # Find contours in the center mask
        center_contours, _ = cv2.findContours(center_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in center_contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)

            # Only proceed if the area is above the threshold
            if area > self.area_threshold:
                # Extract the bright red region (potential laser center)
                roi_center = frame[y:y+h, x:x+w]
                
                # Calculate brightness and ensure it is very high (indicating laser core)
                gray_center = cv2.cvtColor(roi_center, cv2.COLOR_BGR2GRAY)
                center_brightness = np.mean(gray_center)
                
                if center_brightness < self.brightness_threshold:
                    continue  # Skip non-bright regions
                
                # Check surrounding area for gradual red decrease
                outer_region_found = self.check_outer_region(hsv, x, y, w, h)
                
                if outer_region_found:
                    # Draw a green rectangle around detected laser pointer region
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Estimate the distance to the laser
                    distance = self.estimate_distance(w)
                    
                    # Annotate the distance on the frame
                    cv2.putText(frame, f"Distance: {distance:.2f} m", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame

    def check_outer_region(self, hsv, x, y, w, h):
        """Check for a gradually fading red region around the center."""
        outer_layers = [
            {"lower": np.array([0, 100, 100]), "upper": np.array([10, 200, 200]), "dilation": 3},
            {"lower": np.array([0, 70, 50]), "upper": np.array([10, 150, 150]), "dilation": 5},
        ]
        
        for layer in outer_layers:
            # Create a mask for the outer red layers
            mask_outer = cv2.inRange(hsv, layer["lower"], layer["upper"])
            mask_outer = apply_dilation(mask_outer, iterations=layer["dilation"])
            
            # Check if there are sufficient red pixels around the detected center
            roi_outer = mask_outer[y:y+h, x:x+w]
            red_pixel_ratio = np.sum(roi_outer) / (w * h * 255)  # Ratio of red pixels in the outer area

            # Require at least 15% red pixels in the outer layer to confirm
            if red_pixel_ratio < 0.15:
                return False
        
        return True

    def estimate_distance(self, pixel_width):
        """Estimate the distance to the laser based on its pixel width."""
        focal_length = CAMERA_PARAMS["focal_length"]
        real_laser_diameter = CAMERA_PARAMS["real_laser_diameter"]
        distance = (real_laser_diameter * focal_length) / pixel_width
        return distance
