from utils.video_stream import VideoStream
from detection.laser_detector import LaserDetector
import cv2

def main():
    # 初始化视频流和激光检测器
    video_stream = VideoStream().start()
    detector = LaserDetector()

    while True:
        # 从视频流获取帧
        frame = video_stream.read()
        
        if frame is None:
            break

        # 检测激光点并框选
        processed_frame, distance = detector.detect_laser(frame)

        # 显示结果
        cv2.imshow("Laser Detection", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    video_stream.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
