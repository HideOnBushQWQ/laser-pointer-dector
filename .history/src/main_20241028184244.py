# src/main.py

import cv2
from utils.video_stream import open_video_stream, read_frame
from detection.laser_detector import detect_laser_pointer

def main():
    cap = open_video_stream()

    while True:
        frame = read_frame(cap)

        # Detect the laser pointer and get bounding box and distance
        bounding_box, distance, area = detect_laser_pointer(frame)

        if bounding_box is not None:
            x, y, w, h = bounding_box

            # Draw a green rectangle around the detected laser spot
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the distance if within the specified range
            if distance and 1.9 <= distance <= 2.1:
                cv2.putText(frame, f"Distance: {distance:.2f} m", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Label the laser pointer
            cv2.putText(frame, "Laser Pointer", (x, y - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Laser Pointer Detection', frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
