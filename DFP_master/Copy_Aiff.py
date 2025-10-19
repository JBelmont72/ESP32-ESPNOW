'''
## Coyy .aiff files onto MAC desktop folder
* File:  /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFP_master/Copy_Aiff.py
* Function: copy .aiff files from CDs onto  Mac, but instead of overwriting or duplicating numbers (1.aiff, 2.aiff, etc.), you want to:
Choose the starting number for each batch of files you copy (so e.g. CD1 can be 1.aiff, 2.aiff... but CD2 could start at 51.aiff etc.).
Keep a dictionary where the key is the new number you assign (1, 2, 51, …) and the value is the original filename from the CD (Track 01.aiff, Beethoven Symphony 5.aiff, etc.).

How this works:
When you insert a new CD and copy its .aiff files into a temporary folder (e.g., ~/Desktop/CD1), run this script.
Set start_number to the next available number. (If your last CD ended at 50, set it to 51.)
It copies .aiff files into your master folder (~/Desktop/All_AIFF) with sequential numbering (51.aiff, 52.aiff, …).
It also creates a dictionary (mapping_dict) and saves it as a mapping.txt file for reference. Example:
1: Track 01.aiff
2: Track 02.aiff
3: Beethoven Symphony 5.aiff


'''
import os
import shutil

def copy_and_rename_aiff(source_dir, dest_dir, start_num=1):
    """
    Copies .aiff files from source_dir to dest_dir, renames them starting 
    from start_num, and builds a dictionary mapping new numbers to original names.

    Args:
        source_dir (str): Path where CD .aiff files are located
        dest_dir (str): Path where renamed .aiff files will be saved
        start_num (int): The starting number for renaming

    Returns:
        dict: Mapping of new numbers (int) → original filenames (str)
    """
    mapping = {}
    current_num = start_num
    
    # Ensure destination folder exists
    os.makedirs(dest_dir, exist_ok=True)
    
    # Process only .aiff files
    for filename in sorted(os.listdir(source_dir)):
        if filename.lower().endswith(".aiff"):
            original_path = os.path.join(source_dir, filename)
            new_name = f"{current_num}.aiff"
            new_path = os.path.join(dest_dir, new_name)
            
            # Copy and rename
            shutil.copy2(original_path, new_path)
            
            # Add to dictionary
            mapping[current_num] = filename
            print(f"Copied {filename} → {new_name}")
            
            current_num += 1
    
    return mapping


# === Example usage ===
if __name__ == "__main__":
    source = "/Users/yourname/Desktop/CD1"   # folder with original AIFF files
    dest = "/Users/yourname/Desktop/All_AIFF" # master folder for all renamed AIFF
    # source = "/Users/yourname/Desktop/CD1"   # folder with original AIFF files
    # dest = "/Users/yourname/Desktop/All_AIFF" # master folder for all renamed AIFF
    start_number = 1   # change this before running each CD
    
    mapping_dict = copy_and_rename_aiff(source, dest, start_number)
    
    # Save mapping dictionary for later reference
    with open(os.path.join(dest, "mapping.txt"), "w") as f:
        for k, v in mapping_dict.items():
            f.write(f"{k}: {v}\n")
