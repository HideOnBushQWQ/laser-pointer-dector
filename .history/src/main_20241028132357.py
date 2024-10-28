# main.py
import sys
import os
import cv2
from utils.video_stream import VideoStream
from detection.laser_detector import LaserDetector
from config import RED_LOWER, RED_UPPER, BRIGHTNESS_THRESHOLD, MIN_AREA, MAX_AREA

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def main():
    video_stream = VideoStream()  # init camera
    detector = LaserDetector(RED_LOWER, RED_UPPER, BRIGHTNESS_THRESHOLD, MIN_AREA, MAX_AREA)

    while True:
        frame = video_stream.get_frame()
        if frame is None:
            break

        # detect
        detected, coordinates, bounding_box, distance = detector.detect(frame)
        if detected:
            # 画出绿色矩形框
            x, y, w, h = bounding_box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 显示距离信息
            cv2.putText(frame, f"{distance} m", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

        # 显示视频流
        cv2.imshow("Laser Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()