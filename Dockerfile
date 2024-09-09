# Use official Python image as a base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including OpenGL libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY yolov5/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the YOLOv5 repo
COPY yolov5 /app/yolov5

# Copy the inference script
COPY inference.py /app

# Set the command to run the inference script
CMD ["python", "inference.py"]
