# src/utils/video_stream.py

import cv2

def open_video_stream():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Error: Could not open video device.")
    return cap

def read_frame(cap):
    ret, frame = cap.read()
    if not ret:
        raise IOError("Failed to capture frame.")
    return frame
