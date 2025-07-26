#!/usr/bin/env python3
"""
Advanced Face Detection GUI App
Features: Real-time detection, image processing, settings adjustment, and more
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import os
import time

class FaceDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Face Detection App")
        self.root.geometry("900x700")
        
        # Initialize variables
        self.cap = None
        self.detection_active = False
        self.current_frame = None
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # Detection parameters
        self.scale_factor = tk.DoubleVar(value=1.1)
        self.min_neighbors = tk.IntVar(value=5)
        self.min_size = tk.IntVar(value=30)
        
        # Statistics
        self.total_faces_detected = 0
        self.frames_processed = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Face Detection App", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Left panel - Controls
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Webcam controls
        webcam_frame = ttk.LabelFrame(controls_frame, text="Webcam", padding="5")
        webcam_frame.pack(fill="x", pady=(0, 10))
        
        self.start_btn = ttk.Button(webcam_frame, text="Start Webcam", 
                                   command=self.start_webcam)
        self.start_btn.pack(fill="x", pady=2)
        
        self.stop_btn = ttk.Button(webcam_frame, text="Stop Webcam", 
                                  command=self.stop_webcam, state="disabled")
        self.stop_btn.pack(fill="x", pady=2)
        
        self.capture_btn = ttk.Button(webcam_frame, text="Capture Frame", 
                                     command=self.capture_frame, state="disabled")
        self.capture_btn.pack(fill="x", pady=2)
        
        # Image controls
        image_frame = ttk.LabelFrame(controls_frame, text="Image Processing", padding="5")
        image_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(image_frame, text="Load Image", 
                  command=self.load_image).pack(fill="x", pady=2)
        
        ttk.Button(image_frame, text="Save Current View", 
                  command=self.save_image).pack(fill="x", pady=2)
        
        # Detection parameters
        params_frame = ttk.LabelFrame(controls_frame, text="Detection Parameters", padding="5")
        params_frame.pack(fill="x", pady=(0, 10))
        
        # Scale Factor
        ttk.Label(params_frame, text="Scale Factor:").pack(anchor="w")
        scale_scale = ttk.Scale(params_frame, from_=1.05, to=2.0, 
                               variable=self.scale_factor, orient="horizontal")
        scale_scale.pack(fill="x", pady=2)
        scale_label = ttk.Label(params_frame, textvariable=self.scale_factor)
        scale_label.pack(anchor="w")
        
        # Min Neighbors
        ttk.Label(params_frame, text="Min Neighbors:").pack(anchor="w", pady=(10, 0))
        neighbors_scale = ttk.Scale(params_frame, from_=1, to=10, 
                                   variable=self.min_neighbors, orient="horizontal")
        neighbors_scale.pack(fill="x", pady=2)
        neighbors_label = ttk.Label(params_frame, textvariable=self.min_neighbors)
        neighbors_label.pack(anchor="w")
        
        # Min Size
        ttk.Label(params_frame, text="Min Face Size:").pack(anchor="w", pady=(10, 0))
        size_scale = ttk.Scale(params_frame, from_=20, to=100, 
                              variable=self.min_size, orient="horizontal")
        size_scale.pack(fill="x", pady=2)
        size_label = ttk.Label(params_frame, textvariable=self.min_size)
        size_label.pack(anchor="w")
        
        # Statistics
        stats_frame = ttk.LabelFrame(controls_frame, text="Statistics", padding="5")
        stats_frame.pack(fill="x")
        
        self.stats_text = tk.Text(stats_frame, height=6, width=30)
        self.stats_text.pack(fill="both", expand=True)
        
        # Center panel - Video display
        video_frame = ttk.LabelFrame(main_frame, text="Video/Image Display", padding="10")
        video_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.video_label = ttk.Label(video_frame, text="No video/image loaded", 
                                    relief="sunken", anchor="center")
        self.video_label.pack(fill="both", expand=True)
        
        # Right panel - Face details
        faces_frame = ttk.LabelFrame(main_frame, text="Detected Faces", padding="10")
        faces_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        self.faces_listbox = tk.Listbox(faces_frame, height=15)
        self.faces_listbox.pack(fill="both", expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief="sunken", anchor="w")
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def start_webcam(self):
        """Start webcam detection"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                return
            
            self.detection_active = True
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.capture_btn.config(state="normal")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
            self.detection_thread.daemon = True
            self.detection_thread.start()
            
            self.status_var.set("Webcam active - detecting faces...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start webcam: {str(e)}")
    
    def stop_webcam(self):
        """Stop webcam detection"""
        self.detection_active = False
        if self.cap:
            self.cap.release()
        
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.capture_btn.config(state="disabled")
        self.status_var.set("Webcam stopped")
    
    def webcam_detection_loop(self):
        """Main webcam detection loop"""
        while self.detection_active:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            self.current_frame = frame.copy()
            processed_frame = self.detect_faces(frame)
            
            # Convert to PIL Image and display
            self.display_frame(processed_frame)
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.03)
    
    def detect_faces(self, frame):
        """Detect faces in a frame and return processed frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces with current parameters
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor.get(),
            minNeighbors=self.min_neighbors.get(),
            minSize=(self.min_size.get(), self.min_size.get())
        )
        
        # Draw rectangles and face numbers
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f'Face {i+1}', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Update statistics
        self.frames_processed += 1
        self.total_faces_detected += len(faces)
        
        # Update faces list and statistics
        self.root.after(0, self.update_face_list, faces)
        self.root.after(0, self.update_statistics, len(faces))
        
        return frame
    
    def display_frame(self, frame):
        """Display frame in the GUI"""
        # Resize frame for display
        height, width = frame.shape[:2]
        max_width, max_height = 400, 300
        
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image and then to PhotoImage
        pil_image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(pil_image)
        
        # Update label
        self.root.after(0, lambda: self.video_label.configure(image=photo))
        self.root.after(0, lambda: setattr(self.video_label, 'image', photo))
    
    def update_face_list(self, faces):
        """Update the faces listbox"""
        self.faces_listbox.delete(0, tk.END)
        for i, (x, y, w, h) in enumerate(faces):
            self.faces_listbox.insert(tk.END, f"Face {i+1}: ({x},{y}) {w}x{h}")
    
    def update_statistics(self, current_faces):
        """Update statistics display"""
        stats = f"Current Faces: {current_faces}\n"
        stats += f"Total Faces: {self.total_faces_detected}\n"
        stats += f"Frames Processed: {self.frames_processed}\n"
        if self.frames_processed > 0:
            avg_faces = self.total_faces_detected / self.frames_processed
            stats += f"Avg Faces/Frame: {avg_faces:.2f}\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def load_image(self):
        """Load and process an image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            try:
                image = cv2.imread(file_path)
                if image is None:
                    messagebox.showerror("Error", "Could not load image")
                    return
                
                self.current_frame = image.copy()
                processed_image = self.detect_faces(image)
                self.display_frame(processed_image)
                
                self.status_var.set(f"Loaded image: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def save_image(self):
        """Save the current processed frame"""
        if self.current_frame is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        
        if file_path:
            try:
                processed_frame = self.detect_faces(self.current_frame.copy())
                cv2.imwrite(file_path, processed_frame)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
                self.status_var.set(f"Saved: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def capture_frame(self):
        """Capture current webcam frame"""
        if self.current_frame is not None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"face_capture_{timestamp}.jpg"
            try:
                processed_frame = self.detect_faces(self.current_frame.copy())
                cv2.imwrite(filename, processed_frame)
                messagebox.showinfo("Success", f"Frame captured as {filename}")
                self.status_var.set(f"Captured: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to capture frame: {str(e)}")
    
    def __del__(self):
        """Cleanup when app is closed"""
        if self.cap:
            self.cap.release()

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = FaceDetectionGUI(root)
    
    # Handle window close event
    def on_closing():
        if app.detection_active:
            app.stop_webcam()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()