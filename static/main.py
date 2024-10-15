import os
import shutil

def copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copies the contents of source_dir to dest_dir.
    First, it clears the contents of dest_dir to ensure a clean copy.
    
    Args:
        source_dir (str): Path to the source directory.
        dest_dir (str): Path to the destination directory.
    """
    # Check if the destination directory exists
    if os.path.exists(dest_dir):
        # Remove everything in the destination directory
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Recreate the destination directory
    os.mkdir(dest_dir)
    print(f"Created destination directory: {dest_dir}")

    # Copy contents from source to destination
    for item in os.listdir(source_dir):
        # Create full path to source item
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)

        if os.path.isdir(source_item):
            # If the item is a directory, create the corresponding directory in dest and recurse
            print(f"Creating directory: {dest_item}")
            os.mkdir(dest_item)
            copy_directory_contents(source_item, dest_item)  # Recursive call
        else:
            # If the item is a file, copy it to the destination
            print(f"Copying file: {source_item} to {dest_item}")
            shutil.copy(source_item, dest_item)


def main():
    # Source and destination directories
    source_directory = "static"
    destination_directory = "public"
    
    # Call the function to copy contents
    copy_directory_contents(source_directory, destination_directory)
    print("Static content successfully copied to public directory!")
