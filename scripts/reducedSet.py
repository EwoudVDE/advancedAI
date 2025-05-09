# File paths (adjust if needed)
defined_ts_path = "DefinedTS/list_defined_TS.txt"
annotation_files = [
    "BelgiumTSD_annotations/BTSD_training_GTclear.txt",
    "BelgiumTSD_annotations/BTSD_testing_GTclear.txt"
]
output_path = "annotations.txt"

# Step 1: Parse DefinedTS list
defined_ts_map = {}
with open(defined_ts_path, "r") as f:
    lines = f.read().splitlines()

for i in range(0, len(lines), 2):
    class_id = int(lines[i])
    filename = lines[i + 1].replace(".png", "")
    defined_ts_map[filename] = class_id

# Step 2: Reduced class names
reduced_class_ids = {
    "A13", "A14", "A15", "A1A", "A1B", "A1C", "A1D", "A23", "A25", "A29", "A31", "A33", "A41", "A51",
    "A7A", "A7B", "A7C", "B15A", "B17", "B1", "B19", "B5", "C1", "C11", "C21", "C23", "C27", "C29", "C3",
    "C31LEFT", "C31RIGHT", "C35", "C43", "D10", "D1a", "D1b", "D3b", "D5", "D7", "D9", "E1", "E3", "E5", "E7",
    "B21", "E9a", "E9a_miva", "E9b", "E9c", "E9d", "E9e", "F12a", "F12b", "F19", "F45", "F47", "F49", "F50",
    "F59", "F87", "B11", "B9"
}

# Step 3: Get allowed class IDs
allowed_class_ids = {defined_ts_map[name] for name in reduced_class_ids if name in defined_ts_map}

# Step 4: Combine and filter annotations
filtered = []
for file_path in annotation_files:
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) >= 6:
                try:
                    class_id = int(parts[5])
                    if class_id in allowed_class_ids:
                        filtered.append(line)
                except ValueError:
                    continue  # Skip malformed lines

# Step 5: Save filtered annotations
with open(output_path, "w") as f:
    f.writelines(filtered)

print(f"Combined filtered annotations saved to {output_path}. Total entries: {len(filtered)}")
