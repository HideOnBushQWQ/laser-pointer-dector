# src/config.py

# Threshold values for detecting the laser pointer
THRESHOLDS = {
    "brightness_threshold": 70,  # Further reduced brightness threshold
    "red_intensity_threshold": 120,  # Adjusted red intensity threshold
    "area_threshold": 20,  # Reduced area size of the red region to capture smaller spots
}

# Camera parameters for distance estimation
CAMERA_PARAMS = {
    "focal_length": 800,
    "real_laser_diameter": 0.005,
}
