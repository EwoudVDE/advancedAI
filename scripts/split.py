import os
import shutil
import random
from collections import defaultdict
from tqdm import tqdm

random.seed(42)

# Directories
images_root = 'images'
labels_root = 'labels'
output_dir = 'dataset'
train_ratio = 0.8

# Discover all image-label pairs and their class IDs
image_to_classes = {}
class_to_images = defaultdict(set)

for subdir in sorted(os.listdir(labels_root)):
    label_subdir = os.path.join(labels_root, subdir)
    if not os.path.isdir(label_subdir):
        continue

    for label_file in os.listdir(label_subdir):
        if not label_file.endswith('.txt'):
            continue

        base_name = os.path.splitext(label_file)[0]
        label_path = os.path.join(label_subdir, label_file)
        image_rel_path = os.path.join(subdir, base_name + '.jp2')
        image_path = os.path.join(images_root, image_rel_path)

        if not os.path.exists(image_path):
            continue

        classes = set()
        with open(label_path, 'r') as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    classes.add(class_id)
                    class_to_images[class_id].add(image_rel_path)

        image_to_classes[image_rel_path] = classes

# Stratified split
train_set = set()
val_set = set()

for class_id, image_names in class_to_images.items():
    image_list = list(image_names)
    random.shuffle(image_list)
    n_train = max(1, int(len(image_list) * train_ratio))

    train_set.update(image_list[:n_train])
    val_set.update(image_list[n_train:])

# Fill in remainder
remaining = set(image_to_classes.keys()) - train_set - val_set
remaining = list(remaining)
random.shuffle(remaining)
n_train = int(len(remaining) * train_ratio)

train_set.update(remaining[:n_train])
val_set.update(remaining[n_train:])

# Copy function
def copy_set(image_set, split):
    img_dst = os.path.join(output_dir, split, 'images')
    lbl_dst = os.path.join(output_dir, split, 'labels')
    os.makedirs(img_dst, exist_ok=True)
    os.makedirs(lbl_dst, exist_ok=True)

    for rel_path in tqdm(image_set, desc=f'Copying {split}'):
        # Copy image
        src_img = os.path.join(images_root, rel_path)
        dst_img = os.path.join(img_dst, os.path.basename(rel_path))
        shutil.copy(src_img, dst_img)

        # Copy label
        label_rel = rel_path.replace('.jp2', '.txt')
        src_lbl = os.path.join(labels_root, label_rel)
        dst_lbl = os.path.join(lbl_dst, os.path.basename(label_rel))
        if os.path.exists(src_lbl):
            shutil.copy(src_lbl, dst_lbl)

# Perform copy
copy_set(train_set, 'train')
copy_set(val_set, 'val')

print(f"\n✅ Done. {len(train_set)} images in train, {len(val_set)} in val.")
