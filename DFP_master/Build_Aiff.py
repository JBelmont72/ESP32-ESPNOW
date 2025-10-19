'''
chat [rename and map aiff](https://chatgpt.com/c/68de97b8-652c-8324-91cb-db4fa5387f76)
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFP_master/Build_Aiff.py
## standalone program that does just first step of building the Music folder with .aiff files:
* You rip a CD → .aiff files go into a 'CD' folder on your Desktop.
* You run the script → it moves them into a 'Music' folder, renames them sequentially as .aiff starting from a number you choose.
* Later you’ll use another program for mapping names and for .mp3 conversion to SD card
* this program is used to build the .aiff containing 'Music' folder with sequential numbers that i will later use in tow ways.
* 1. to build a clean SD card using DFP_Tools and 2. Copy_Aiff.py for mapping the file numbers with names!

CD is the file where i load the original CD, 
then make a copy using cp -R source destination and name it CD_backup or CD2_bakup etc
The back up keeps the original so I do not lose it 
Music is the folder where the sequentially 01 ....10...etc .aiff files go

5 October 2025 current count of files is 134 so start at 135 next use
most recent terminal output:  Copied & mapped: 5 Lucy In The Sky With Diamonds.aiff → 130.aiff
🎵 Copied & mapped: 6 A Day In The Life.aiff → 131.aiff
🎵 Copied & mapped: 7 All You Need Is Love.aiff → 132.aiff
🎵 Copied & mapped: 8 I Am The Walrus.aiff → 133.aiff
🎵 Copied & mapped: 9 Hello, Goodbye.aiff → 134.aiff
✅ Copy + rename complete!
📘 Updated track map saved to: /Users/judsonbelmont/Desktop/music_map.json
(.venv) judsonbelmont@MacBook-Pro ESP32-ESPNOW % 
'''
import os
import shutil
import json

def copy_number_and_map_aiff(cd_folder, music_folder, map_file, start_number=1):
    """
    Copy AIFF files from cd_folder → music_folder,
    renaming both copies sequentially starting at start_number,
    and updating a dictionary mapping {number: original name}.
    """
    # 🗂️ Verify folders
    if not os.path.exists(cd_folder):
        print(f"❌ CD folder not found: {cd_folder}")
        return
    
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)
        print(f"📁 Created music folder: {music_folder}")

    # 📖 Load existing map if it exists
    if os.path.exists(map_file):
        with open(map_file, "r") as f:
            track_map = json.load(f)
        # Convert keys back to int (JSON saves them as strings)
        track_map = {int(k): v for k, v in track_map.items()}
        print(f"📘 Loaded existing track map with {len(track_map)} entries.")
    else:
        track_map = {}

    # Determine next available number automatically if start_number = 0
    if start_number == 0 and track_map:
        start_number = max(track_map.keys()) + 1
        print(f"🔢 Auto-starting at {start_number} based on existing map.")
    elif start_number == 0:
        start_number = 1

    current_num = start_number

    for file in sorted(os.listdir(cd_folder)):
        if file.lower().endswith(".aiff"):
            src = os.path.join(cd_folder, file)
            base_name = f"{current_num}.aiff"
            dst = os.path.join(music_folder, base_name)
            renamed_src = os.path.join(cd_folder, base_name)

            # Avoid overwriting in Music folder
            while os.path.exists(dst) or current_num in track_map:
                current_num += 1
                base_name = f"{current_num}.aiff"
                dst = os.path.join(music_folder, base_name)
                renamed_src = os.path.join(cd_folder, base_name)

            # 1️⃣ Copy original to Music
            shutil.copy2(src, dst)

            # 2️⃣ Rename file in CD folder
            os.rename(src, renamed_src)

            # 3️⃣ Add mapping
            track_map[current_num] = file

            print(f"🎵 Copied & mapped: {file} → {base_name}")
            current_num += 1

    # 4️⃣ Save updated dictionary
    with open(map_file, "w") as f:
        json.dump(track_map, f, indent=4)

    print(f"✅ Copy + rename complete!")
    print(f"📘 Updated track map saved to: {map_file}")


if __name__ == "__main__":
    home = os.path.expanduser("~")
    # cd_folder = os.path.join(home, "Desktop", "RollingStone2")
    cd_folder = os.path.join(home, "Desktop", "Beatles_67to70")
    # cd_folder = os.path.join(home, "Desktop", "Beatles_1")
    # cd_folder = os.path.join(home, "Desktop", "TheWho")
    music_folder = os.path.join(home, "Desktop", "Music")
    map_file = os.path.join(home, "Desktop", "music_map.json")

    print("💿 Copy AIFF files to Music folder and update song map.")
    print("💡 Tip: Enter 0 to auto-start numbering after your last track.")

    try:
        start_num = int(input("Enter starting number (or 0 for auto): "))
    except ValueError:
        start_num = 0

    copy_number_and_map_aiff(cd_folder, music_folder, map_file, start_num)
    
'''
 
 Perfect — this next version makes your workflow *future-proof and modular.* 🎵

It does everything the last version did, **plus:**
✅ If `music_map.json` already exists, it **loads it first** and adds new entries.
✅ No duplicates — it checks for existing keys and skips or renumbers as needed.
✅ Keeps the numbering continuous (starting wherever you want).

Here’s the refined script:

---

```python
import os
import shutil
import json

def copy_number_and_map_aiff(cd_folder, music_folder, map_file, start_number=1):
    """
    Copy AIFF files from cd_folder → music_folder,
    renaming both copies sequentially starting at start_number,
    and updating a dictionary mapping {number: original name}.
    """
    # 🗂️ Verify folders
    if not os.path.exists(cd_folder):
        print(f"❌ CD folder not found: {cd_folder}")
        return
    
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)
        print(f"📁 Created music folder: {music_folder}")

    # 📖 Load existing map if it exists
    if os.path.exists(map_file):
        with open(map_file, "r") as f:
            track_map = json.load(f)
        # Convert keys back to int (JSON saves them as strings)
        track_map = {int(k): v for k, v in track_map.items()}
        print(f"📘 Loaded existing track map with {len(track_map)} entries.")
    else:
        track_map = {}

    # Determine next available number automatically if start_number = 0
    if start_number == 0 and track_map:
        start_number = max(track_map.keys()) + 1
        print(f"🔢 Auto-starting at {start_number} based on existing map.")
    elif start_number == 0:
        start_number = 1

    current_num = start_number

    for file in sorted(os.listdir(cd_folder)):
        if file.lower().endswith(".aiff"):
            src = os.path.join(cd_folder, file)
            base_name = f"{current_num}.aiff"
            dst = os.path.join(music_folder, base_name)
            renamed_src = os.path.join(cd_folder, base_name)

            # Avoid overwriting in Music folder
            while os.path.exists(dst) or current_num in track_map:
                current_num += 1
                base_name = f"{current_num}.aiff"
                dst = os.path.join(music_folder, base_name)
                renamed_src = os.path.join(cd_folder, base_name)

            # 1️⃣ Copy original to Music
            shutil.copy2(src, dst)

            # 2️⃣ Rename file in CD folder
            os.rename(src, renamed_src)

            # 3️⃣ Add mapping
            track_map[current_num] = file

            print(f"🎵 Copied & mapped: {file} → {base_name}")
            current_num += 1

    # 4️⃣ Save updated dictionary
    with open(map_file, "w") as f:
        json.dump(track_map, f, indent=4)

    print(f"✅ Copy + rename complete!")
    print(f"📘 Updated track map saved to: {map_file}")


if __name__ == "__main__":
    home = os.path.expanduser("~")
    cd_folder = os.path.join(home, "Desktop", "CD")
    music_folder = os.path.join(home, "Desktop", "Music")
    map_file = os.path.join(home, "Desktop", "music_map.json")

    print("💿 Copy AIFF files to Music folder and update song map.")
    print("💡 Tip: Enter 0 to auto-start numbering after your last track.")

    try:
        start_num = int(input("Enter starting number (or 0 for auto): "))
    except ValueError:
        start_num = 0

    copy_number_and_map_aiff(cd_folder, music_folder, map_file, start_num)
```

---

### ✅ Summary of new features:

* **Keeps `music_map.json` cumulative.**
* **Auto-continue** numbering if you enter `0` at the prompt.
* **Safe overwriting:** skips numbers already used.
* Renames in both folders for consistency.
* Easy to import the map later:

  ```python
  import json
  with open("/Users/yourname/Desktop/music_map.json") as f:
      song_map = json.load(f)
  ```

---

Would you like the script to also **print a running summary** at the end (like total tracks and last assigned number)?
That’s useful for checking where to start next time when doing manual numbering.

 
 
 '''   

