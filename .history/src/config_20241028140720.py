# Color range for detecting red laser in HSV color space
# Adjusted for detecting laser's surrounding area
RED_LOWER = (0, 150, 100)   # Lower bound for red color in HSV
RED_UPPER = (10, 255, 255)  # Upper bound for red color in HSV

# Brightness threshold for detecting the laser's high-intensity core
BRIGHTNESS_THRESHOLD = 200  # Minimum brightness for core detection

# Area constraints for detected laser region to filter out noise
MIN_AREA = 10    # Minimum area for detected red region (in pixels)
MAX_AREA = 500   # Maximum area for detected red region (in pixels)

# Focal length for distance estimation (in pixels)
# Adjust based on the specific camera's calibration
FOCAL_LENGTH = 500

# Continuous detection requirements
REQUIRED_CONSECUTIVE_FRAMES = 3  # Number of consecutive frames for reliable detection
COORDINATE_THRESHOLD = 10  # Pixel distance threshold for consecutive detection

