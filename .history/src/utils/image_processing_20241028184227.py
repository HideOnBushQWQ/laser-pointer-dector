# src/utils/image_processing.py

import cv2
import numpy as np
from config import RED_LOWER1, RED_UPPER1, RED_LOWER2, RED_UPPER2

def get_red_mask(hsv_frame):
    mask1 = cv2.inRange(hsv_frame, RED_LOWER1, RED_UPPER1)
    mask2 = cv2.inRange(hsv_frame, RED_LOWER2, RED_UPPER2)
    return cv2.bitwise_or(mask1, mask2)

def apply_blur(mask):
    return cv2.GaussianBlur(mask, (9, 9), 0)
