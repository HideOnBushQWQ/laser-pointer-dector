# image_processing.py
import cv2

def apply_erosion(image, iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.erode(image, kernel, iterations=iterations)

def apply_dilation(image, iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.dilate(image, kernel, iterations=iterations)
