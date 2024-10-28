# src/config.py

# Threshold values for detecting the laser pointer
THRESHOLDS = {
    "brightness_threshold": 200,  # Brightness threshold for laser core
    "red_intensity_threshold": 150,  # Minimum red intensity for red regions
    "area_threshold": 50,  # Minimum area size of the red region
}

# Camera parameters for distance estimation
CAMERA_PARAMS = {
    "focal_length": 800,  # Focal length of the camera in pixels
    "real_laser_diameter": 0.005,  # Real diameter of the laser dot in meters
}
