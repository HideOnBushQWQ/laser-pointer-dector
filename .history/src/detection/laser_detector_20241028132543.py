import cv2
import numpy as np
from utils.image_processing import apply_erosion, apply_dilation


class LaserDetector:
    def __init__(self, red_lower, red_upper, brightness_threshold, min_area, max_area, focal_length=500):
        self.red_lower = red_lower
        self.red_upper = red_upper
        self.brightness_threshold = brightness_threshold
        self.min_area = min_area
        self.max_area = max_area
        self.focal_length = focal_length 
        
    def detect(self, frame):
        # HSV space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # red laser
        mask = cv2.inRange(hsv, self.red_lower, self.red_upper)
        mask = apply_erosion(mask)
        mask = apply_dilation(mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area <= area <= self.max_area:
                x, y, w, h = cv2.boundingRect(contour)
                coordinates = (x + w // 2, y + h // 2)
                distance = self.calculate_distance(w) 
                return True, coordinates, (x, y, w, h), distance

        return False, None, None, None  # not found

    def calculate_distance(self, width):
        known_width = 0.01
        distance = (known_width * self.focal_length) / width
        return round(distance, 2)  # 返回米，保留两位小数
