import os

folder_path = 'G:/project/dataset/val/images'

deleted = 0
for file in os.listdir(folder_path):
    if file.endswith('.npy'):
        file_path = os.path.join(folder_path, file)
        os.remove(file_path)
        deleted += 1

print(f"Deleted {deleted} .npy file(s) from {folder_path}")
