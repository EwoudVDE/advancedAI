from ultralytics import YOLO
import sys
import os

# Add the ultralytics repo to the Python path (if using custom local version)
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "external", "ultralytics"))


if __name__ == "__main__":
    # Load custom model architecture or pretrained model
    model = YOLO("yolov8-CBAM.yaml")  # or "yolov8n.pt" for default small model

    # Start training
    results = model.train(
        data="data.yaml",
        epochs=300,
        imgsz=1024,
        batch=12,
        patience=30,
        device=0,
        pretrained=True,
        fliplr=0.0,
        optimizer='AdamW',  # delete this line if you want to use the default optimizer
        close_mosaic=30,
        warmup_epochs=3
    )
