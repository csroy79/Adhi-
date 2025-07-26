#!/usr/bin/env python3
"""
Simple Face Detection App using OpenCV
Supports both webcam detection and image file detection
"""

import cv2
import sys
import os

def detect_faces_in_image(image_path, output_path=None):
    """
    Detect faces in a static image file
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return False
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the face detection classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Add face coordinates text
        cv2.putText(image, f'Face {len(faces)}', (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Save the result
    if output_path is None:
        output_path = f"detected_{os.path.basename(image_path)}"
    
    cv2.imwrite(output_path, image)
    print(f"Detected {len(faces)} face(s) in the image")
    print(f"Result saved as: {output_path}")
    
    return True

def detect_faces_webcam():
    """
    Real-time face detection using webcam
    """
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return False
    
    # Load the face detection classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    print("Starting webcam face detection...")
    print("Press 'q' to quit, 'c' to capture frame, 's' to save current frame")
    
    frame_count = 0
    capture_count = 0
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame from webcam")
            break
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw rectangles around detected faces
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Add face number
            cv2.putText(frame, f'Face {i+1}', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add info text
        cv2.putText(frame, f'Faces: {len(faces)} | Frame: {frame_count}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to quit, 'c' to capture", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display the resulting frame
        cv2.imshow('Face Detection', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c') or key == ord('s'):
            # Capture current frame
            capture_filename = f"capture_{capture_count:03d}.jpg"
            cv2.imwrite(capture_filename, frame)
            print(f"Frame captured: {capture_filename}")
            capture_count += 1
        
        frame_count += 1
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print(f"Webcam session ended. Processed {frame_count} frames.")
    
    return True

def main():
    """
    Main function to handle command line arguments and run face detection
    """
    print("Face Detection App")
    print("=" * 50)
    
    # Check for help argument first
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['--help', '-h', 'help']:
        print("Face Detection App Help")
        print("=" * 30)
        print("This app can detect faces in real-time using your webcam or in static images.")
        print()
        print("Usage:")
        print("1. Webcam mode (default):")
        print("   python face_detection_simple.py")
        print("   python face_detection_simple.py webcam")
        print("   - Press 'q' to quit")
        print("   - Press 'c' or 's' to capture current frame")
        print()
        print("2. Image mode:")
        print("   python face_detection_simple.py path/to/image.jpg [output_path.jpg]")
        print("   - If output_path is not provided, saves as 'detected_filename.jpg'")
        print()
        print("Requirements:")
        print("- OpenCV (cv2)")
        print("- NumPy")
        print("- A webcam for real-time detection")
        return
    
    if len(sys.argv) == 1:
        # No arguments - use webcam
        print("No arguments provided. Starting webcam face detection...")
        detect_faces_webcam()
    
    elif len(sys.argv) == 2:
        # One argument - could be 'webcam' or image file path
        arg = sys.argv[1].lower()
        if arg == 'webcam':
            print("Starting webcam face detection...")
            detect_faces_webcam()
        else:
            # Assume it's an image file path
            image_path = sys.argv[1]
            if not os.path.exists(image_path):
                print(f"Error: Image file '{image_path}' not found")
                return
            
            print(f"Detecting faces in image: {image_path}")
            output_path = f"detected_{os.path.basename(image_path)}"
            detect_faces_in_image(image_path, output_path)
    
    elif len(sys.argv) == 3:
        # Two arguments - input and output paths
        image_path, output_path = sys.argv[1], sys.argv[2]
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            return
        
        print(f"Detecting faces in image: {image_path}")
        print(f"Output will be saved to: {output_path}")
        detect_faces_in_image(image_path, output_path)
    
    else:
        print("Usage:")
        print("  python face_detection_simple.py                    # Use webcam")
        print("  python face_detection_simple.py webcam             # Use webcam explicitly")
        print("  python face_detection_simple.py <image_path>       # Detect in image")
        print("  python face_detection_simple.py <input> <output>   # Detect and save")
        print("  python face_detection_simple.py --help             # Show help")

if __name__ == "__main__":
    main()