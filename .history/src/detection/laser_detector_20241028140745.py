import cv2
import numpy as np
from utils.image_processing import apply_erosion, apply_dilation

class LaserDetector:
    def __init__(self):
        # Initialize detection thresholds from config
        self.red_lower = RED_LOWER
        self.red_upper = RED_UPPER
        self.brightness_threshold = BRIGHTNESS_THRESHOLD
        self.min_area = MIN_AREA
        self.max_area = MAX_AREA
        self.focal_length = FOCAL_LENGTH

        # Continuous detection variables
        self.consecutive_frames = 0
        self.required_consecutive_frames = REQUIRED_CONSECUTIVE_FRAMES
        self.last_coordinates = None
    def detect(self, frame):
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Step 1: Detect a larger red area (surrounding area of the laser)
        mask_wide = cv2.inRange(hsv, self.red_lower, self.red_upper)
        mask_wide = apply_erosion(mask_wide)
        mask_wide = apply_dilation(mask_wide)

        # Find contours within the wide area mask
        contours, _ = cv2.findContours(mask_wide, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)

            # Check if the area and aspect ratio match laser characteristics
            if self.min_area <= area <= self.max_area and 0.9 <= w/h <= 1.1:
                # Step 2: Within the detected red area, apply brightness filtering to find the laser core
                mask_core = mask_wide[y:y+h, x:x+w]
                v_channel = hsv[y:y+h, x:x+w, 2]  # Extract the brightness channel for the region
                core_mask = cv2.bitwise_and(mask_core, mask_core, mask=(v_channel > self.brightness_threshold).astype(np.uint8) * 255)

                # If there are valid pixels in the core area, consider it as laser detection
                if cv2.countNonZero(core_mask) > 0:
                    coordinates = (x + w // 2, y + h // 2)  # Center coordinates of the laser
                    distance = self.calculate_distance(w)   # Estimate the distance

                    # Check for continuous detection
                    if self.is_continuous_detection(coordinates):
                        return True, coordinates, (x, y, w, h), distance

        # No laser detected, reset continuous detection state
        self.reset_detection()
        return False, None, None, None

    def calculate_distance(self, width):
        # Estimate distance using known focal length and width
        known_width = 0.01  # Assume the actual laser width is 1 cm
        distance = (known_width * self.focal_length) / width
        return round(distance, 2)  # Return distance in meters, rounded to 2 decimal places

    def is_continuous_detection(self, coordinates, threshold=10):
        # Check if the detected laser position is close to the previous position
        if self.last_coordinates and self.is_close(coordinates, self.last_coordinates, threshold):
            self.consecutive_frames += 1
        else:
            self.consecutive_frames = 1  # New position detected, reset consecutive frames count
        self.last_coordinates = coordinates

        # Return True if required consecutive frames threshold is met
        return self.consecutive_frames >= self.required_consecutive_frames

    def is_close(self, coord1, coord2, threshold=10):
        # Determine if two coordinates are within a given threshold
        return abs(coord1[0] - coord2[0]) < threshold and abs(coord1[1] - coord2[1]) < threshold

    def reset_detection(self):
        # Reset continuous detection state
        self.consecutive_frames = 0
        self.last_coordinates = None
