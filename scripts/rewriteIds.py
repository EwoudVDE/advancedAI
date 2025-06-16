import os

# Directories where label files are located (train and val)
LABEL_DIRS = ['dataset/train/labels', 'dataset/val/labels']

# Old format (current IDs)
OLD_CLASSES = {
    1: "A11", 2: "A13", 3: "A14", 4: "A15", 5: "A17", 6: "A19", 7: "A1A", 8: "A1B", 9: "A1C", 10: "A1D", 
    11: "A21", 12: "A23", 13: "A25", 14: "A27", 15: "A29", 16: "A3", 17: "A31", 18: "A33", 19: "A35", 20: "A37", 
    21: "A39", 22: "A41", 23: "A43", 24: "A49", 25: "A5", 26: "A51", 27: "A7A", 28: "A7B", 29: "A7C", 30: "A9", 
    31: "B1", 32: "B11", 33: "B13", 34: "B15A", 35: "B17", 36: "B19", 37: "B21", 38: "B3", 39: "B5", 40: "B7", 
    41: "B9", 42: "C1", 43: "C11", 44: "C13", 45: "C15", 46: "C17", 47: "C19", 48: "C21", 49: "C22", 50: "C23", 
    51: "C24a", 52: "C24b", 53: "C24c", 54: "C25", 55: "C27", 56: "C29", 57: "C3", 58: "C31LEFT", 59: "C31RIGHT", 
    60: "C33", 61: "C35", 62: "C37", 63: "C39", 64: "C41", 65: "C43", 66: "C45", 67: "C47n", 68: "C48", 69: "C5", 
    70: "C7", 71: "C9", 72: "D10", 73: "D11", 74: "D13", 75: "D1a", 76: "D1b", 77: "D1e", 78: "D3b", 79: "D5", 
    80: "D7", 81: "D9", 82: "E1", 83: "E11", 84: "E3", 85: "E5", 86: "E7", 87: "E9a", 88: "E9a_bewoners", 89: "E9a_disk", 
    90: "E9a_miva", 91: "E9ag7dn-2", 92: "E9ag7dn-3", 93: "E9ag7dn", 94: "E9b", 95: "E9c", 96: "E9d", 97: "E9e", 
    98: "E9f", 99: "E9g", 100: "E9h", 101: "E9i", 102: "F1", 103: "F101a", 104: "F101b", 105: "F101c", 106: "F103n", 
    107: "F105n", 108: "F107", 109: "F109", 110: "F11", 111: "F12a", 112: "F12b", 113: "F13", 114: "F14", 115: "F15", 
    116: "F17", 117: "F18", 118: "F19", 119: "F1a_h", 120: "F1a_v", 121: "F1b_h", 122: "F1b_v", 123: "F21", 124: "F23A", 
    125: "F23B", 126: "F23C", 127: "F23D", 128: "F25", 129: "F27", 130: "F29", 131: "F31", 132: "F33B", 133: "F33C", 
    134: "F33a", 135: "F34A", 136: "F34B1", 137: "F34B2", 138: "F34C1", 139: "F34C2", 140: "F35", 141: "F37", 142: "F39", 
    143: "F3a_h", 144: "F3a_v", 145: "F3b_h", 146: "F3b_v", 147: "F41", 148: "F43", 149: "F45", 150: "F47", 151: "F49", 
    152: "F4a", 153: "F4b", 154: "F5", 155: "F50", 156: "F50bis", 157: "F51A", 158: "F51B", 159: "F53", 160: "F55", 
    161: "F56", 162: "F57", 163: "F59", 164: "F60", 165: "F61", 166: "F62", 167: "F63", 168: "F65", 169: "F67", 170: "F69", 
    171: "F7", 172: "F71", 173: "F73", 174: "F75", 175: "F77", 176: "F79", 177: "F8", 178: "F81", 179: "F83", 180: "F85", 
    181: "F87", 182: "F89", 183: "F9", 184: "F91", 185: "F93", 186: "F95", 187: "F97B", 188: "F98", 189: "F98onder", 
    190: "F99a", 191: "F99b", 192: "F99c", 193: "Handic", 194: "begin", 195: "betalend", 196: "bewoners-betalend", 
    197: "bewoners", 198: "disk", 199: "e0c", 200: "einde", 201: "lang", 202: "m1", 203: "m2", 204: "m3", 205: "m4", 
    206: "m5", 207: "m6", 208: "m7", 209: "m8", 210: "typeII"
}

# New format (reduced class IDs)
NEW_CLASSES = {
    0: "A13", 1: "A14", 2: "A15", 3: "A1A", 4: "A1B", 5: "A1C", 6: "A1D", 7: "A23", 8: "A25", 9: "A29", 10: "A31", 
    11: "A33", 12: "A41", 13: "A51", 14: "A7A", 15: "A7B", 16: "A7C", 17: "B1", 18: "B11", 19: "B15A", 20: "B17", 
    21: "B19", 22: "B21", 23: "B5", 24: "B9", 25: "C1", 26: "C11", 27: "C21", 28: "C23", 29: "C27", 30: "C29", 31: "C3", 
    32: "C31LEFT", 33: "C31RIGHT", 34: "C35", 35: "C43", 36: "D10", 37: "D1a", 38: "D1b", 39: "D3b", 40: "D5", 41: "D7", 
    42: "D9", 43: "E1", 44: "E3", 45: "E5", 46: "E7", 47: "E9a", 48: "E9a_miva", 49: "E9b", 50: "E9c", 51: "E9d", 
    52: "E9e", 53: "F12a", 54: "F12b", 55: "F19", 56: "F45", 57: "F47", 58: "F49", 59: "F50", 60: "F59", 61: "F87"
}

def remap_labels():
    for label_dir in LABEL_DIRS:
        for filename in os.listdir(label_dir):
            # Check if the file has a .txt extension (label file)
            if filename.endswith('.txt'):
                file_path = os.path.join(label_dir, filename)
                
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                with open(file_path, 'w') as file:
                    for line in lines:
                        parts = line.strip().split(' ')
                        old_class = int(parts[0])
                        if old_class in OLD_CLASSES:
                            # Map the old class to the new class
                            new_class_name = OLD_CLASSES[old_class]
                            if new_class_name in NEW_CLASSES.values():
                                new_class_id = list(NEW_CLASSES.keys())[list(NEW_CLASSES.values()).index(new_class_name)]
                                parts[0] = str(new_class_id)
                        file.write(' '.join(parts) + '\n')

# Run the remapping function
remap_labels()
