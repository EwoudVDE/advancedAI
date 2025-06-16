import os
from PIL import Image
from pathlib import Path

# ---------------------------------------
# Paths
# ---------------------------------------

# File containing filtered annotations (semicolon-separated)
annotations_file = 'annotations.txt'

# Root directory containing the original images
image_root = 'images'

# Target directory to save YOLO-format labels
labels_root = 'labels'

# Ensure the labels directory exists
os.makedirs(labels_root, exist_ok=True)

# ---------------------------------------
# Read and Process Each Annotation
# ---------------------------------------

# Load all annotation lines from file
with open(annotations_file, 'r') as f:
    lines = f.readlines()

# Loop over each line to convert annotations
for line in lines:
    parts = line.strip().split(';')

    # Ensure line has at least 7 fields (image path + bbox + class)
    if len(parts) < 7:
        continue

    # Extract fields from annotation
    image_path_rel = parts[0]  # relative path to image
    xmin, ymin, xmax, ymax = map(float, parts[1:5])
    class_id = int(parts[5])   # integer class ID

    # Resolve the full path to the image file
    image_path = os.path.join(image_root, image_path_rel)
    if not os.path.exists(image_path):
        print(f"⚠️ Image not found: {image_path}")
        continue

    # Load image to get original width and height
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    # ---------------------------------------
    # Convert Bounding Box to YOLO Format
    # ---------------------------------------
    # YOLO format: <class> <x_center> <y_center> <width> <height>
    # All values must be normalized (0.0 to 1.0)

    x_center = ((xmin + xmax) / 2) / img_width
    y_center = ((ymin + ymax) / 2) / img_height
    box_width = (xmax - xmin) / img_width
    box_height = (ymax - ymin) / img_height

    # Format the label line
    yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"

    # ---------------------------------------
    # Save Label File
    # ---------------------------------------

    # Convert image path to corresponding .txt label path
    label_path = os.path.join(labels_root, Path(image_path_rel).with_suffix('.txt'))

    # Ensure directory exists (for nested paths)
    os.makedirs(os.path.dirname(label_path), exist_ok=True)

    # Append the line to the label file
    with open(label_path, 'a') as lf:
        lf.write(yolo_line + '\n')

print("✅ Conversion to YOLO format complete.")
