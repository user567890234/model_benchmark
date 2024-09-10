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
    # Path to the 'videos' folder inside the container
    video_dir = Path("/app/videos")
    
    # List video files from the 'videos' directory
    video_paths = list(video_dir.glob("*.mp4"))  # Assuming .mp4 videos
    
    # Output paths for processed videos
    output_paths = [f"/app/output_video{i+1}.mp4" for i in range(len(video_paths))]
    
    for video_path, output_path in zip(video_paths, output_paths):
        print(f"Processing {video_path}...")
        process_video(video_path, output_path)
        print(f"Saved processed video to {output_path}")

if __name__ == "__main__":
    main()
