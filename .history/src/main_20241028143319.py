# main.py
import cv2
from utils.video_stream import get_video_stream
from detection.laser_detector import detect_laser_point

def main():
    cap = get_video_stream()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect laser point
        laser_center, bounding_box, distance = detect_laser_point(frame)
        
        if laser_center:
            # Draw bounding box
            x, y, w, h = bounding_box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Label distance
            label = f"Distance: {distance:.2f} m"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow("Laser Detection", frame)
        
        
        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
