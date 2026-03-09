import os
import glob

# Base path for the pest dataset
base_dir = "D:/sih_vision_workspace/pest"
splits = ['train', 'valid', 'test']

def shift_labels(label_dir, shift_amount=2):
    if not os.path.exists(label_dir):
        print(f"Skipping: Directory not found -> {label_dir}")
        return

    txt_files = glob.glob(os.path.join(label_dir, "*.txt"))
    if not txt_files:
        print(f"Warning: No .txt files found in {label_dir}")
        return
        
    for file_path in txt_files:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0:
                # Shift the class ID
                original_class = int(parts[0])
                new_class = original_class + shift_amount
                parts[0] = str(new_class)
                new_lines.append(" ".join(parts) + "\n")
                
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
            
    print(f"Successfully shifted {len(txt_files)} files in {label_dir}.")

for split in splits:
    target_dir = f"{base_dir}/{split}/labels"
    shift_labels(target_dir)