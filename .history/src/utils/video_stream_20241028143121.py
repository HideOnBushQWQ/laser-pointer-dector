# video_stream.py
import cv2

def get_video_stream():
    # Open the default camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    return cap
