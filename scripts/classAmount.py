import os

# Directories for your train and validation labels
train_labels_dir = 'dataset/train/labels'
val_labels_dir = 'dataset/val/labels'

# List all label files in the train and validation directories
train_label_files = [os.path.join(train_labels_dir, f) for f in os.listdir(train_labels_dir) if f.endswith('.txt')]
val_label_files = [os.path.join(val_labels_dir, f) for f in os.listdir(val_labels_dir) if f.endswith('.txt')]

# Initialize a dictionary to store class occurrences for train and val
train_class_counts = {i: 0 for i in range(62)}  # Assuming 62 classes
val_class_counts = {i: 0 for i in range(62)}  # Assuming 62 classes

# Function to count class occurrences in a label file
def count_classes_in_label_file(label_file, class_counts):
    with open(label_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            class_id = int(line.split()[0])  # Class ID is the first number in each line
            class_counts[class_id] += 1

# Count the occurrences of each class in the training label files
for label_file in train_label_files:
    count_classes_in_label_file(label_file, train_class_counts)

# Count the occurrences of each class in the validation label files
for label_file in val_label_files:
    count_classes_in_label_file(label_file, val_class_counts)

# Print the occurrences of each class in training and validation sets
print("Class Occurrences in Training Labels:")
for class_id, count in train_class_counts.items():
    print(f"Class {class_id}: {count} occurrences")

print("\nClass Occurrences in Validation Labels:")
for class_id, count in val_class_counts.items():
    print(f"Class {class_id}: {count} occurrences")