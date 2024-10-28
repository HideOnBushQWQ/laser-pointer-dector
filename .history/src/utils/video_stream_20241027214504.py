import cv2


class VideoStream:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # 打开默认摄像头

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
