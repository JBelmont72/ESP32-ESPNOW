def explain_folder_track(folder, track):
    """
    Show how DFPlayer builds the PARAM and command packet
    from folder and track numbers.
    """
    param = (folder << 8) | track
    high = (param >> 8) & 0xFF
    low  = param & 0xFF

    print("=== DFPlayer Folder/Track Command ===")
    print(f"Folder: {folder} (dec) = {folder:#04x} (hex) = {folder:08b} (bin)")
    print(f"Track : {track} (dec) = {track:#04x} (hex) = {track:08b} (bin)")
    print()
    print(f"PARAM = (folder << 8) | track = {param} (dec) = {param:#06x} (hex)")
    print(f"PARAM binary = {param:016b}")
    print(f"  High byte (folder) = {high:#04x} ({high:08b})")
    print(f"  Low  byte (track)  = {low:#04x} ({low:08b})")
    print()
    # Build the full 10-byte command
    buf = [
        0x7E, 0xFF, 0x06, 0x0F, 0x00,
        high, low,
        0x00, 0x00, 0xEF
    ]
    print("Full UART packet to DFPlayer:")
    print(" ".join(f"{b:02X}" for b in buf))
    print("====================================")
    print()
# Example: Folder 12 (C), Track 3 to use:
explain_folder_track(12, 3)

# Example: Folder 1, Track 1
# 7E FF 06 0F 00 0C 03 00 00 EF
explain_folder_track(1, 1)
# for (12,3): Full UART packet to DFPlayer:
# 7E FF 06 0F 00 01 01 00 00 EF