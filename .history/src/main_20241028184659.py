# src/main.py

import cv2
from config import THRESHOLDS
from utils.video_stream import VideoStream
from detection.laser_detector import LaserDetector

def main():
    # Initialize video stream and laser detector
    video_stream = VideoStream()
    laser_detector = LaserDetector(THRESHOLDS)
    
    # Start video processing
    while True:
        frame = video_stream.get_frame()
        if frame is None:
            break

        # Detect laser pointer in the frame
        output_frame = laser_detector.detect_laser(frame)
        
        # Display the result
        cv2.imshow("Laser Pointer Detection", output_frame)
        
        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
