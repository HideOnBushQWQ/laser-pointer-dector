from utils.video_stream import VideoStream
from detection.laser_detector import LaserDetector
import cv2

def main():
    video_stream = VideoStream()  # Initialize camera
    detector = LaserDetector()    # No arguments needed here

    while True:
        frame = video_stream.get_frame()
        if frame is None:
            break

        # Detect laser position and distance
        detected, coordinates, bounding_box, distance = detector.detect(frame)
        if detected:
            # Draw a green rectangle around the detected laser
            x, y, w, h = bounding_box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display distance information
            cv2.putText(frame, f"{distance} m", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 255, 0), 2)

        # Display the video stream
        cv2.imshow("Laser Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
