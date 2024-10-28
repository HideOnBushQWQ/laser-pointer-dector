# src/config.py

# Threshold values for detecting the laser pointer
THRESHOLDS = {
    "brightness_threshold": 100,   # Slightly lower brightness threshold to capture bright center
    "red_intensity_threshold": 150,  # Higher red intensity threshold to focus on intense red
    "area_threshold": 20,  # Lower area threshold for smaller laser point regions
    "max_area_threshold": 100,  # New: Maximum area to filter out larger non-laser regions like lips
}

# Camera parameters for distance estimation
CAMERA_PARAMS = {
    "focal_length": 800,  # Focal length of the camera in pixels
    "real_laser_diameter": 0.005,  # Real diameter of the laser dot in meters
}
