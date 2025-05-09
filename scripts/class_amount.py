from collections import defaultdict

# Path to your annotation file
annotation_file = "annotations.txt"

# Dictionary to hold counts
class_counts = defaultdict(int)
label_counts = defaultdict(int)

# Whether your file contains class labels (the 12th field)
HAS_LABELS = True

with open(annotation_file, "r") as f:
    for line in f:
        parts = line.strip().split(";")
        if len(parts) < 6:
            continue  # skip invalid lines
        class_id = int(parts[5])
        class_counts[class_id] += 1

        if HAS_LABELS and len(parts) >= 12:
            class_label = parts[11].strip()
            label_counts[class_label] += 1

# Print class ID counts
print("Annotations per class ID:")
for class_id in sorted(class_counts.keys()):
    print(f"Class ID {class_id}: {class_counts[class_id]} annotations")

# Print class label counts (optional)
if HAS_LABELS:
    print("\nAnnotations per class label:")
    for label in sorted(label_counts.keys()):
        print(f"Label {label}: {label_counts[label]} annotations")
