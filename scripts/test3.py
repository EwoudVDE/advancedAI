import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Define your paths
image_folder = './dataset/train/images'
annotation_folder = './dataset/train/labels'
target_image = 'image.000002.jp2'

# Construct the full paths
image_path = os.path.join(image_folder, target_image)
label_path = os.path.join(annotation_folder, target_image.replace('.jp2', '.txt'))

# Read the image
image = Image.open(image_path)

# Read the YOLO label file (class id, x_center, y_center, width, height)
with open(label_path, 'r') as file:
    labels = file.readlines()

# Convert image size to pixel dimensions
image_width, image_height = image.size

# Draw the bounding boxes
draw = ImageDraw.Draw(image)

for label in labels:
    # Parse the label data
    parts = label.strip().split()
    class_id = int(parts[0])  # This is the class id
    x_center = float(parts[1]) * image_width  # Convert normalized x_center to pixels
    y_center = float(parts[2]) * image_height  # Convert normalized y_center to pixels
    width = float(parts[3]) * image_width  # Convert normalized width to pixels
    height = float(parts[4]) * image_height  # Convert normalized height to pixels

    # Calculate the bounding box coordinates
    left = x_center - width / 2
    top = y_center - height / 2
    right = x_center + width / 2
    bottom = y_center + height / 2

    # Draw the bounding box
    draw.rectangle([left, top, right, bottom], outline="red", width=2)

# Show the image with bounding boxes
plt.imshow(image)
plt.axis('off')  # Hide axis
plt.show()
