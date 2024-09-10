import torch
from pathlib import Path
import cv2
import os 

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def process_video(video_path, output_path):
    # Open video file
    cap = cv2.VideoCapture(str(video_path))
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Create a VideoWriter object to save the output video
    out = cv2.VideoWriter(str(output_path), codec, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Inference
        results = model(frame)
        
        # Render results on the frame
        frame = results.render()[0]
        
        # Write the frame to the output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()

def main():
    # Directory containing videos
    video_dir = '/app/videos'  # Adjust the path to /app/videos
    
    # List of video files in the directory
    video_paths = [os.path.join(video_dir, i) for i in os.listdir(video_dir) if i.endswith('.mp4')]

    # Output paths for processed videos
    output_paths = [f"/app/output_video{i+1}.mp4" for i in range(len(video_paths))]  # Ensure output paths are also within /app
    
    for video_path, output_path in zip(video_paths, output_paths):
        print(f"Processing {video_path}...")
        process_video(video_path, output_path)

