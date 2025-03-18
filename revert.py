import os
import shutil

def revert_organization(o_dir, u_dir):
    if not os.path.exists(o_dir):
        print(f"Organized directory '{o_dir}' does not exist.")
        return
    
    for root, _, files in os.walk(o_dir, topdown=False):  # Bottom-up to delete empty dirs
        for file in files:
            src = os.path.join(root, file)
            dest = os.path.join(u_dir, file)
            try:
                shutil.move(src, dest)
                print(f"Moved {file} back to {u_dir}")
            except Exception as e:
                print(f"Error moving {file}: {e}")
        
        if not os.listdir(root):  # Remove empty directories
            try:
                os.rmdir(root)
                print(f"Removed empty folder: {root}")
            except OSError:
                print(f"Could not remove {root}, might not be empty.")

# Define paths
o_dir = "file_organizer/Organized"
u_dir = "file_organizer/Unorganized"

revert_organization(o_dir, u_dir)
