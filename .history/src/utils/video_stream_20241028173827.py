# src/utils/video_stream.py

import cv2

class VideoStream:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
    
    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def release(self):
        self.cap.release()
