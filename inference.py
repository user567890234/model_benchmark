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
    
    # Define the codec and create a VideoWriter object to save the output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Inference
        results = model(frame)
        
        # Render results on the frame
        frame = results.render()[0]
        
        # Write the processed frame to the output video file
        out.write(frame)

    # Release resources
    cap.release()
    out.release()

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
