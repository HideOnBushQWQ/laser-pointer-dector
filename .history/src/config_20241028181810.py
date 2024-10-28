# src/config.py

# Threshold values for detecting the laser pointer
THRESHOLDS = {
    "brightness_threshold": 120,  # Lowered brightness threshold
    "red_intensity_threshold": 120,  # Adjusted red intensity threshold
    "area_threshold": 50,  # Minimum area size of the red region
}

# Camera parameters for distance estimation
CAMERA_PARAMS = {
    "focal_length": 800,
    "real_laser_diameter": 0.005,
}
