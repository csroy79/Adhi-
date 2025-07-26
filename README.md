# Face Detection App

A comprehensive Python-based face detection application using OpenCV with both command-line and GUI interfaces.

## Features

### Simple Command-Line Version (`face_detection_simple.py`)
- Real-time face detection using webcam
- Face detection in static images
- Command-line interface with multiple usage modes
- Automatic saving of processed images
- Frame capture functionality

### Advanced GUI Version (`face_detection_gui.py`)
- Modern tkinter-based graphical user interface
- Real-time webcam face detection with live preview
- Load and process image files
- Adjustable detection parameters (scale factor, min neighbors, min size)
- Statistics tracking (total faces detected, frames processed)
- Frame capture and image saving functionality
- Face coordinates display
- Professional UI with organized panels

## Installation

1. **Clone or download this repository**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify OpenCV installation:**
   ```bash
   python -c "import cv2; print(cv2.__version__)"
   ```

## Usage

### Simple Command-Line Version

#### 1. Webcam Detection (Default)
```bash
python face_detection_simple.py
```
- Starts real-time face detection using your webcam
- Press 'q' to quit
- Press 's' to save the current frame

#### 2. Image File Detection
```bash
python face_detection_simple.py path/to/your/image.jpg
```
- Detects faces in the specified image
- Automatically saves the result as `detected_[original_filename]`

#### 3. Custom Output Path
```bash
python face_detection_simple.py input_image.jpg output_image.jpg
```
- Detects faces in input image and saves to specified output path

### Advanced GUI Version

```bash
python face_detection_gui.py
```

#### GUI Features:
- **Webcam Controls**: Start/stop webcam, capture frames
- **Image Processing**: Load images, save processed results
- **Detection Parameters**: Adjust detection sensitivity in real-time
  - Scale Factor: Controls detection accuracy (1.05 - 2.0)
  - Min Neighbors: Minimum detection confirmations (1 - 10)
  - Min Face Size: Minimum face size in pixels (20 - 100)
- **Statistics**: Real-time tracking of detection performance
- **Face List**: Displays coordinates and dimensions of detected faces

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- NumPy
- Pillow (PIL)
- tkinter (usually included with Python)

## How It Works

The application uses OpenCV's Haar Cascade Classifier for face detection:

1. **Image Preprocessing**: Converts input to grayscale for processing
2. **Face Detection**: Uses `haarcascade_frontalface_default.xml` classifier
3. **Result Visualization**: Draws bounding rectangles around detected faces
4. **Parameter Tuning**: Adjustable parameters for different scenarios:
   - `scaleFactor`: How much the image size is reduced at each scale
   - `minNeighbors`: How many neighbors each face should retain
   - `minSize`: Minimum possible face size

## Troubleshooting

### Common Issues:

1. **Webcam not working:**
   - Check if camera is connected and not being used by another application
   - Try changing camera index in code (0, 1, 2, etc.)

2. **OpenCV installation issues:**
   ```bash
   pip install --upgrade opencv-python
   ```

3. **GUI not displaying properly:**
   - Ensure tkinter is installed (usually comes with Python)
   - On Linux: `sudo apt-get install python3-tk`

4. **Poor detection accuracy:**
   - Adjust detection parameters in the GUI version
   - Ensure good lighting conditions
   - Make sure faces are clearly visible and frontal

## File Structure

```
face-detection-app/
├── requirements.txt              # Python dependencies
├── face_detection_simple.py      # Command-line version
├── face_detection_gui.py         # GUI version
├── README.md                     # This file
└── [generated files]             # Captured frames and processed images
```

## Examples

### Example Output Files:
- `face_detection_frame_0001.jpg` - Captured webcam frames
- `detected_your_image.jpg` - Processed image files
- `face_capture_20231201_143022.jpg` - Timestamped captures

## Advanced Usage

### Customizing Detection Parameters:
- **Lower scaleFactor** (1.05-1.1): More accurate but slower
- **Higher minNeighbors** (5-8): Fewer false positives
- **Larger minSize**: Ignore very small faces

### Performance Tips:
- Use smaller input images for faster processing
- Adjust webcam resolution if needed
- Close other applications using the camera

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Future Enhancements

Potential features for future versions:
- Multiple face detection models (DNN-based)
- Face recognition capabilities
- Emotion detection
- Age and gender estimation
- Video file processing
- Batch image processing
- Export detection data to CSV