import torch
from pathlib import Path
import cv2
import os

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def process_video(video_path):
    # Open video file
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Inference
        results = model(frame)
        
        # Render results on the frame
        frame = results.render()[0]
        
        # Display the frame
        cv2.imshow('Processed Frame', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Path to the 'videos' folder inside the container
    video_dir = Path("/app/videos")
    
    # List video files from the 'videos' directory
    video_paths = list(video_dir.glob("*.mp4"))  # Assuming .mp4 videos
    
    if not video_paths:
        print("No video files found in the directory.")
        return
    
    for video_path in video_paths:
        print(f"Processing {video_path}...")
        process_video(video_path)
        print(f"Finished processing {video_path}")

if __name__ == "__main__":
    main()
