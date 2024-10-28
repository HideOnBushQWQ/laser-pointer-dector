import cv2
import numpy as np
from config import RED_LOWER, RED_UPPER, MIN_AREA, MAX_AREA, FOCAL_LENGTH, REQUIRED_CONSECUTIVE_FRAMES, COORDINATE_THRESHOLD

class LaserDetector:
    def __init__(self):
        # Initialize detection thresholds from config
        self.red_lower = RED_LOWER
        self.red_upper = RED_UPPER
        self.min_area = MIN_AREA
        self.max_area = MAX_AREA
        self.focal_length = FOCAL_LENGTH
        self.required_consecutive_frames = REQUIRED_CONSECUTIVE_FRAMES
        self.consecutive_frames = 0
        self.last_coordinates = None

    def detect(self, frame):
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)

        # Convert to HSV color space for color filtering
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        hsv_mask = cv2.inRange(hsv, self.red_lower, self.red_upper)

        # Convert to LAB color space for brightness filtering
        lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, _ = cv2.split(lab)

        # Use adaptive threshold on the L channel to capture bright spots
        _, bright_mask = cv2.threshold(l_channel, 200, 255, cv2.THRESH_BINARY)

        # Combine HSV red mask with LAB brightness mask
        combined_mask = cv2.bitwise_and(hsv_mask, bright_mask)

        # Erode and dilate to remove noise
        combined_mask = cv2.erode(combined_mask, None, iterations=2)
        combined_mask = cv2.dilate(combined_mask, None, iterations=2)

        # Find contours and filter based on area and circularity
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area <= area <= self.max_area:
                # Check circularity to confirm laser shape
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * (area / (perimeter * perimeter))
                    if 0.7 <= circularity <= 1.2:  # Adjust for circular shapes
                        x, y, w, h = cv2.boundingRect(contour)
                        coordinates = (x + w // 2, y + h // 2)
                        distance = self.calculate_distance(w)

                        if self.is_continuous_detection(coordinates):
                            return True, coordinates, (x, y, w, h), distance

        self.reset_detection()
        return False, None, None, None

    def calculate_distance(self, width):
        known_width = 0.01  # Assume laser dot is about 1 cm wide
        return round((known_width * self.focal_length) / width, 2)

    def is_continuous_detection(self, coordinates, threshold=COORDINATE_THRESHOLD):
        if self.last_coordinates and self.is_close(coordinates, self.last_coordinates, threshold):
            self.consecutive_frames += 1
        else:
            self.consecutive_frames = 1
        self.last_coordinates = coordinates
        return self.consecutive_frames >= self.required_consecutive_frames

    def is_close(self, coord1, coord2, threshold):
        return abs(coord1[0] - coord2[0]) < threshold and abs(coord1[1] - coord2[1]) < threshold

    def reset_detection(self):
        self.consecutive_frames = 0
        self.last_coordinates = None
