import os
from PIL import Image
from pathlib import Path

# Paths
annotations_file = 'annotations.txt'
image_root = 'images'
labels_root = 'labels'

# Create labels folder structure
os.makedirs(labels_root, exist_ok=True)

# Read annotations.txt
with open(annotations_file, 'r') as f:
    lines = f.readlines()

for line in lines:
    parts = line.strip().split(';')
    if len(parts) < 7:
        continue

    image_path_rel = parts[0]
    xmin, ymin, xmax, ymax = map(float, parts[1:5])
    class_id = int(parts[5])

    # Full path to image
    image_path = os.path.join(image_root, image_path_rel)
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        continue

    # Load image to get dimensions
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    # Convert to YOLO format
    x_center = ((xmin + xmax) / 2) / img_width
    y_center = ((ymin + ymax) / 2) / img_height
    box_width = (xmax - xmin) / img_width
    box_height = (ymax - ymin) / img_height

    yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"

    # Save label file
    label_path = os.path.join(labels_root, Path(image_path_rel).with_suffix('.txt'))
    os.makedirs(os.path.dirname(label_path), exist_ok=True)
    with open(label_path, 'a') as lf:
        lf.write(yolo_line + '\n')

print("✅ Conversion complete.")
