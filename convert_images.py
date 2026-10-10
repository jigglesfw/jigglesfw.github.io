import os
from psd_tools import PSDImage
import tkinter as tk
from tkinter import filedialog

def convert_psd_to_png(input_path):
    try:
        output_path = os.path.splitext(input_path)[0] + ".png"
        psd = PSDImage.open(input_path)
        composite = psd.composite()
        composite.save(output_path, "PNG")
        print(f"Successfully converted: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def main():
    # Initialize hidden tkinter root window
    root = tk.Tk()
    root.withdraw()

    print("Opening file selection window...")
    
    # Open file dialog allowing multiple .psd file selections
    file_paths = filedialog.askopenfilenames(
        title="Select PSD files to convert",
        filetypes=[("Photoshop files", "*.psd"), ("All files", "*.*")]
    )

    if not file_paths:
        print("No files selected. Exiting.")
        return

    print(f"Found {len(file_paths)} file(s) to convert.")
    
    for file_path in file_paths:
        if file_path.lower().endswith(".psd"):
            convert_psd_to_png(file_path)
        else:
            print(f"Skipping non-PSD file: {os.path.basename(file_path)}")

    print("Conversion process complete!")

if __name__ == "__main__":
    main()