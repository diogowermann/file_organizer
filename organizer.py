import os
import shutil

def organize_files(source_folder, destination_folder, rules):
    """
    Organizes files based on user-defined rules.
    
    :param source_folder: Path to the folder where unorganized files are located.
    :param destination_folder: Path where organized files should be moved.
    :param rules: A dictionary where keys are file extensions or names, and values are destination subfolders.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if not os.path.isfile(file_path):
            continue  # Skip directories

        for rule_key, folder_name in rules.items():
            if rule_key.startswith("."):  # Rule is for file extension
                if filename.lower().endswith(rule_key):
                    move_file(file_path, destination_folder, folder_name)
                    break  # Avoid moving the same file twice
            else:  # Rule is for file name matching
                if rule_key.lower() in filename.lower():
                    move_file(file_path, destination_folder, folder_name)
                    break

def move_file(file_path, destination_folder, folder_name):
    """
    Moves a file to the specified folder within the destination directory.
    
    :param file_path: Path of the file to move.
    :param destination_folder: Root destination directory.
    :param folder_name: Name of the subfolder to move the file to.
    """
    target_folder = os.path.join(destination_folder, folder_name)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    try:
        shutil.move(file_path, target_folder)
        print(f"Moved {os.path.basename(file_path)} to {target_folder}")
    except Exception as e:
        print(f"Failed to move {os.path.basename(file_path)} to {target_folder}: {e}")
