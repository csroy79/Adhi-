#!/usr/bin/env python3
"""
Demo script for Face Detection App
Demonstrates both command-line and GUI versions
"""

import os
import sys

def show_demo_menu():
    """
    Display the demo menu and handle user choices
    """
    print("="*60)
    print("        FACE DETECTION APP DEMO")
    print("="*60)
    print()
    print("This demo showcases a complete Python face detection application")
    print("with both command-line and GUI interfaces.")
    print()
    print("Available demos:")
    print("1. Command-line version help")
    print("2. Test image detection (command-line)")
    print("3. Launch GUI version")
    print("4. Show all available files")
    print("5. Exit")
    print()
    
    while True:
        try:
            choice = input("Select demo option (1-5): ").strip()
            
            if choice == '1':
                print("\n" + "="*50)
                print("COMMAND-LINE VERSION HELP")
                print("="*50)
                os.system("python3 face_detection_simple.py --help")
                print()
                
            elif choice == '2':
                print("\n" + "="*50)
                print("TESTING IMAGE DETECTION")
                print("="*50)
                if os.path.exists('test_image.jpg'):
                    print("Using existing test image...")
                    os.system("python3 face_detection_simple.py test_image.jpg demo_output.jpg")
                    print()
                    if os.path.exists('demo_output.jpg'):
                        print("✓ Output saved as 'demo_output.jpg'")
                    print("Note: The test image contains geometric shapes, not real faces,")
                    print("so face detection may not find any faces. Try with a real photo!")
                else:
                    print("Creating test image first...")
                    os.system("python3 create_test_image.py")
                    os.system("python3 face_detection_simple.py test_image.jpg demo_output.jpg")
                print()
                
            elif choice == '3':
                print("\n" + "="*50)
                print("LAUNCHING GUI VERSION")
                print("="*50)
                print("Starting the GUI application...")
                print("Note: GUI may not display properly in headless environments")
                try:
                    os.system("python3 face_detection_gui.py")
                except KeyboardInterrupt:
                    print("\nGUI application closed.")
                print()
                
            elif choice == '4':
                print("\n" + "="*50)
                print("PROJECT FILES")
                print("="*50)
                files = [
                    ('face_detection_simple.py', 'Command-line face detection script'),
                    ('face_detection_gui.py', 'GUI face detection application'),
                    ('requirements.txt', 'Python dependencies'),
                    ('README.md', 'Documentation and usage instructions'),
                    ('haarcascade_frontalface_default.xml', 'OpenCV face detection model'),
                    ('create_test_image.py', 'Test image generator'),
                    ('demo.py', 'This demo script')
                ]
                
                for filename, description in files:
                    status = "✓" if os.path.exists(filename) else "✗"
                    print(f"{status} {filename:<35} - {description}")
                print()
                
            elif choice == '5':
                print("Thank you for trying the Face Detection App!")
                break
                
            else:
                print("Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """
    Main demo function
    """
    print("Python Face Detection App Demo")
    print("Powered by OpenCV")
    print()
    
    # Check dependencies
    missing_deps = []
    try:
        import cv2
    except ImportError:
        missing_deps.append("opencv-python")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    if missing_deps:
        print("Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install missing dependencies and try again.")
        return
    
    # Check if cascade file exists
    if not os.path.exists('haarcascade_frontalface_default.xml'):
        print("Face detection model not found!")
        print("The demo will attempt to download it...")
        os.system("wget -q https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml")
        if os.path.exists('haarcascade_frontalface_default.xml'):
            print("✓ Model downloaded successfully!")
        else:
            print("✗ Failed to download model. Please check internet connection.")
            return
    
    show_demo_menu()

if __name__ == "__main__":
    main()