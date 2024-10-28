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
        
        # Define refined red color range
        lower_red = np.array([0, 100, 50])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # Apply erosion and dilation to reduce noise
        mask = apply_erosion(mask, iterations=2)
        mask = apply_dilation(mask, iterations=2)
        
        # Find contours in the red mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by area and shape ratio
            aspect_ratio = float(w) / h
            if area > self.area_threshold and 0.75 < aspect_ratio < 1.25:
                roi = frame[y:y+h, x:x+w]

                # Calculate brightness, red intensity score, and color channel distribution
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                center_brightness = np.mean(gray_roi)
                
                # Calculate mean red channel intensity in the BGR color space
                mean_red_channel = np.mean(roi[:, :, 2])  # Red channel in BGR
                mean_green_channel = np.mean(roi[:, :, 1])
                mean_blue_channel = np.mean(roi[:, :, 0])

                # Calculate a combined score based on red intensity and brightness
                combined_score = (0.5 * mean_red_channel) + (0.5 * center_brightness)
                
                # Debug output for analysis
                print(f"Detected Region - Position: {(x, y, w, h)}, Area: {area}, Aspect Ratio: {aspect_ratio}, "
                      f"Brightness: {center_brightness}, Red Channel: {mean_red_channel}, "
                      f"Green Channel: {mean_green_channel}, Blue Channel: {mean_blue_channel}, Score: {combined_score}")

                # Filter based on red dominance and combined score
                if combined_score > 100 and mean_red_channel > mean_green_channel + 30 and mean_red_channel > mean_blue_channel + 30:
                    # Draw a green rectangle around detected laser pointer region
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
