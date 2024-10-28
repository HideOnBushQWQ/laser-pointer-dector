# src/utils/image_processing.py

import cv2
import numpy as np

def apply_erosion(image, iterations=1):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)

def apply_dilation(image, iterations=1):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)
