import os
from PIL import Image

# Paths to the train and validation image directories
train_dir = 'dataset/train/images'
val_dir = 'dataset/val/images'

# Function to convert .jp2 to .jpg and delete the original .jp2 files
def convert_and_delete_images(directory):
    # Get all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".jp2"):  # Check for .jp2 files
            img_path = os.path.join(directory, filename)
            try:
                # Open the .jp2 image
                with Image.open(img_path) as img:
                    # Set output path with .jpg extension
                    output_path = os.path.splitext(img_path)[0] + '.jpg'
                    # Convert and save the image
                    img.convert('RGB').save(output_path, 'JPEG')
                
                # Delete the original .jp2 image after conversion
                os.remove(img_path)
                print(f"Converted and deleted {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Convert images in both train and val directories and remove originals
convert_and_delete_images(train_dir)
convert_and_delete_images(val_dir)

print("Image conversion and deletion complete!")
