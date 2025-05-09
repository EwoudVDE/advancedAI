import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Set paths
image_folder = './dataset/train/images'
annotation_file = './BelgiumTSD_annotations/BTSD_testing_GTclear.txt'
defined_ts_file = './DefinedTS/list_defined_TS.txt'
defined_ts_image_folder = './DefinedTS/img'

# Target image
target_image = 'image.000002.jp2'
target_path = os.path.join(image_folder, target_image)

# Step 1: Load the main image
img = Image.open(target_path)

# Step 2: Parse the annotation file and find the matching annotation
bbox = None
class_id = None
with open(annotation_file, 'r') as f:
    for line in f:
        if target_image in line:
            parts = line.strip().split(';')
            x1, y1, x2, y2 = map(float, parts[1:5])
            class_id = int(parts[5])
            bbox = (x1, y1, x2, y2)
            break

if bbox is None:
    print("No annotation found for this image.")
    exit()

# Step 3: Draw bounding box on the main image
img_drawn = img.copy()
draw = ImageDraw.Draw(img_drawn)
draw.rectangle(bbox, outline='red', width=4)
draw.text((bbox[0], bbox[1] - 10), f'Class ID: {class_id}', fill='red')

# Step 4: Parse DefinedTS to find the corresponding sign image
def find_sign_image(class_id):
    with open(defined_ts_file, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            id_line = lines[i].strip()
            if id_line.isdigit() and int(id_line) == class_id:
                img_file = lines[i + 1].strip()
                return os.path.join(defined_ts_image_folder, img_file)
    return None

sign_img_path = find_sign_image(class_id)
sign_img = Image.open(sign_img_path) if sign_img_path else None

# Step 5: Display both images side-by-side
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(img_drawn)
plt.title('Annotated Image')
plt.axis('off')

if sign_img:
    plt.subplot(1, 2, 2)
    plt.imshow(sign_img)
    plt.title(f'Sign ID: {class_id}')
    plt.axis('off')
else:
    print("Sign image not found for class ID:", class_id)

plt.tight_layout()
plt.show()
