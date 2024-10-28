# config.py
# Configuration parameters for laser detection

CONFIG = {
    "brightness_threshold": 200,  # Threshold for brightness to detect laser center
    "red_threshold": (160, 255),  # Threshold for red color in HSV format
    "distance_scale_factor": 0.5,  # Calibration factor for distance estimation
    "dilation_iterations": 2,  # Number of dilation operations
    "erosion_iterations": 1,   # Number of erosion operations
}
