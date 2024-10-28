# src/config.py

# Threshold values for detecting the laser pointer
THRESHOLDS = {
    "brightness_threshold": 100,  # Further lowered brightness threshold
    "red_intensity_threshold": 80,  # Lowered red intensity threshold
    "area_threshold": 50,  # Lowered area threshold to capture smaller regions
}

# Camera parameters for distance estimation
CAMERA_PARAMS = {
    "focal_length": 800,
    "real_laser_diameter": 0.005,
}
