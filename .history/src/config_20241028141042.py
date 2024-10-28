DETECTION_DISTANCE = 2.0
DISTANCE_TOLERANCE = 0.1

# Narrow down the HSV color range for red to focus on the bright center
RED_LOWER = (0, 150, 200)   # Narrower lower bound for bright red
RED_UPPER = (10, 255, 255)  # Upper bound remains high for bright red

BRIGHTNESS_THRESHOLD = 220  # Increase to filter out low-brightness areas

MIN_AREA = 5     # Minimum area of the detected region
MAX_AREA = 200   # Maximum area, adjusted for a small bright spot
FOCAL_LENGTH = 500  # Keep focal length for distance calculation
REQUIRED_CONSECUTIVE_FRAMES = 2  # Reduce consecutive frames if testing indoors
COORDINATE_THRESHOLD = 5         # Smaller threshold to detect similar positions