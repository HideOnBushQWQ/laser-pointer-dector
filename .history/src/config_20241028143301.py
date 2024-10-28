# config.py
# Configuration parameters for laser detection

CONFIG = {
    "brightness_threshold": 250,  # Higher threshold for brightness to detect laser center
    "red_hue_min": 0,             # Minimum hue for red color
    "red_hue_max": 10,            # Maximum hue for red color
    "saturation_min": 100,        # Minimum saturation for red color
    "value_min": 200,             # Minimum value (brightness) for red color
    "distance_scale_factor": 0.5, # Calibration factor for distance estimation
    "dilation_iterations": 2,     # Number of dilation operations
    "erosion_iterations": 1,      # Number of erosion operations
}
