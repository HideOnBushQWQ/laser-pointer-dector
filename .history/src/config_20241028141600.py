DETECTION_DISTANCE = 2.0
DISTANCE_TOLERANCE = 0.1

# Adjusted HSV color range for detecting bright red laser centers
RED_LOWER = (0, 150, 150)   # Narrow lower bound for red hue in HSV
RED_UPPER = (10, 255, 255)  # Upper bound for bright red hue in HSV

# Area constraints for the detected laser region to filter out noise
MIN_AREA = 5     # Minimum area in pixels to capture small laser dots
MAX_AREA = 300   # Maximum area in pixels to avoid larger objects

# Focal length for distance estimation (in pixels)
# Adjust this based on specific camera calibration if necessary
FOCAL_LENGTH = 500

# Continuous detection requirements
REQUIRED_CONSECUTIVE_FRAMES = 2  # Number of frames required for stable detection
COORDINATE_THRESHOLD = 5         # Pixel distance threshold for verifying consecutive positions