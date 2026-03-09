import os
import shutil

WEED_SOURCE = "D:/sih_vision_workspace/weed"
PEST_SOURCE = "D:/sih_vision_workspace/pest"
DEST_ROOT = "D:/sih_vision_workspace/datasets"

def safe_merge(source_base, prefix):
    # Maps your source folder name to the strict YOLO destination folder name
    splits_map = {'train': 'train', 'valid': 'val', 'val': 'val', 'test': 'test'}
    
    for src_split, dest_split in splits_map.items():
        # Check for Roboflow structure (split/images) vs YOLO structure (images/split)
        img_dir_1 = os.path.join(source_base, src_split, 'images')
        lbl_dir_1 = os.path.join(source_base, src_split, 'labels')
        
        img_dir_2 = os.path.join(source_base, 'images', src_split)
        lbl_dir_2 = os.path.join(source_base, 'labels', src_split)
        
        if os.path.exists(img_dir_1):
            src_img_dir, src_lbl_dir = img_dir_1, lbl_dir_1
        elif os.path.exists(img_dir_2):
            src_img_dir, src_lbl_dir = img_dir_2, lbl_dir_2
        else:
            continue # Split doesn't exist in this dataset, move to the next

        dest_img_dir = os.path.join(DEST_ROOT, 'images', dest_split)
        dest_lbl_dir = os.path.join(DEST_ROOT, 'labels', dest_split)
        
        os.makedirs(dest_img_dir, exist_ok=True)
        os.makedirs(dest_lbl_dir, exist_ok=True)

        print(f"Merging {prefix} {src_split} into {dest_split}...")
        
        for filename in os.listdir(src_img_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                base_name = os.path.splitext(filename)[0]
                
                img_src = os.path.join(src_img_dir, filename)
                lbl_src = os.path.join(src_lbl_dir, base_name + ".txt")
                
                img_dest = os.path.join(dest_img_dir, f"{prefix}_{filename}")
                lbl_dest = os.path.join(dest_lbl_dir, f"{prefix}_{base_name}.txt")
                
                shutil.copy(img_src, img_dest)
                if os.path.exists(lbl_src):
                    shutil.copy(lbl_src, lbl_dest)

safe_merge(WEED_SOURCE, "weed")
safe_merge(PEST_SOURCE, "pest")
print("Merge complete! Dataset structure is now YOLO-compliant.")