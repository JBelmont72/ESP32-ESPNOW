
## standalone program that does just first step of building the Music folder with .aiff files:
chat: [rename and map aiff](https://chatgpt.com/c/68de97b8-652c-8324-91cb-db4fa5387f76)
* /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFP_master/Build_Aiff.py

* You rip a CD → .aiff files go into a 'CD' folder on your Desktop.
* You run the script → it moves them into a 'Music' folder, renames them sequentially as .aiff starting from a number you choose.
* Later you’ll use another program for mapping names and for .mp3 conversion to SD card
* this program is used to build the .aiff containing 'Music' folder with sequential numbers that i will later use in tow ways.
* 1. to build a clean SD card using DFP_Tools and 2. Copy_Aiff.py for mapping the file numbers with names!

## Coyy .aiff files onto MAC desktop folder
* File:  /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/           DFP_master/Copy_Aiff.py
* Function: copy .aiff files from CDs onto  Mac, but instead of overwriting or duplicating numbers (1.aiff, 2.aiff, etc.), you want to:
* Choose the starting number for each batch of files you copy (so e.g. CD1 can be 1.aiff, 2.aiff... but CD2 could start at 51.aiff etc.).
* Keep a dictionary where the key is the new number you assign (1, 2, 51, …) and the value is the original filename from the CD (Track 01.aiff, Beethoven Symphony 5.aiff, etc.).
I will load the .aiff files to 'CD' for running the into the folder that will have all the renamed .aiff ( the 'All_AIFF' folder)
on Desktop of old mac pro i have the following folders and purposes:
source = "/Users/yourname/Desktop/CD"   # folder with original AIFF files, 
dest = "/Users/yourname/Desktop/All_AIFF" # master folder for all renamed AIFF
  