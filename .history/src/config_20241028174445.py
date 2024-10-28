# src/config.py

# Threshold values for detecting the laser pointer
THRESHOLDS = {
    "brightness_threshold": 180,  # Reduced brightness threshold for laser core
    "red_intensity_threshold": 140,  # Adjusted red intensity for red regions
    "area_threshold": 30,  # Reduced area size of the red region
}

# Camera parameters for distance estimation
CAMERA_PARAMS = {
    "focal_length": 800,  # Focal length of the camera in pixels
    "real_laser_diameter": 0.005,  # Real diameter of the laser dot in meters
}
