# morph_ops.py
import cv2
import numpy as np
from ..config import KERNEL_SIZE


def apply_erosion(mask):
    kernel = np.ones(KERNEL_SIZE, np.uint8)
    return cv2.erode(mask, kernel, iterations=1)


def apply_dilation(mask):
    kernel = np.ones(KERNEL_SIZE, np.uint8)
    return cv2.dilate(mask, kernel, iterations=1)
