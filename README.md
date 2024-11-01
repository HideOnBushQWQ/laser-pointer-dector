# Laser Pointer Detection

This project is a Python application that uses OpenCV to detect a laser pointer from a webcam feed. It identifies the laser pointer in real-time, draws a green bounding box around it, and displays its distance from the camera (in meters, rounded to two decimal places).


## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- Numpy (`pip install numpy`)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/HideOnBushQWQ/laser-pointer-dector.git
   cd src
   ```

2. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```


## Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. Once the application is running, it will display the webcam feed and attempt to detect any red laser points. When a laser is detected:

   - A circle is drawn around the laser point.

3. To exit the application, press the `q` key.

## Key Features

- **Real-time Laser Detection**: Detects red laser pointers in real-time from the webcam feed.
- **Continuous Detection Filtering**: Ensures that a detection is valid only if the laser pointer is detected consistently across multiple frames to minimize false positives.

## File Descriptions

- **main.py**: The main script that initializes the webcam and continuously processes video frames to detect the laser pointer.
- **config.py**: Holds configurable threshold parameters for laser detection.
- **utils/video_stream.py**: Manages video feed input from the webcam.
- **utils/image_processing.py**: Contains helper functions for image processing, such as erosion and dilation.
- **detection/laser_detector.py**: Implements the core logic for laser pointer detection, including color and brightness filtering, bounding box drawing, and distance calculation.