# Write a Python script that organizes files in your Downloads folder.
import os
import shutil


def organise_downloads():
    download_folder = os.path.expanduser("~/Downloads")

    if not os.path.isdir(download_folder):
        print(f"Downloads folder not found: {download_folder}")
        return

    txt_folder = os.path.join(download_folder, "Text")
    os.makedirs(txt_folder, exist_ok=True)

    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            shutil.move(file_path, os.path.join(txt_folder, filename))


if __name__ == "__main__":
    organise_downloads()