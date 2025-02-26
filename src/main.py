import sys
import os
import shutil
from generate_page import generate_page




def clear_public_directory(public_dir):
    """Clear the public directory."""
    try:
        if os.path.exists(public_dir):
            # Instead of removing the entire directory, let's remove files one by one
            for item in os.listdir(public_dir):
                item_path = os.path.join(public_dir, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except PermissionError:
                    print(f"Warning: Could not remove {item_path} - permission denied")
                    continue
        if not os.path.exists(public_dir):
            os.makedirs(public_dir)
    except Exception as e:
        print(f"Warning: Error clearing public directory: {e}")

def copy_static_files(static_dir, public_dir):
    """Copy static files to the public directory."""
    print(f"Copying static files from {static_dir} to {public_dir}")
    if os.path.exists(static_dir):
        print(f"Static directory exists, contains: {os.listdir(static_dir)}")
        for item in os.listdir(static_dir):
            source = os.path.join(static_dir, item)
            destination = os.path.join(public_dir, item)
            print(f"Copying {source} to {destination}")
            if os.path.isdir(source):
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)
    else:
        print("Warning: Static firectory does not exist!")
        return




def main():
    # Define paths
    
    root_dir = os.getcwd()
      # goes up one level from src/
    public_dir = os.path.join(root_dir, "public")
    static_dir = os.path.join(root_dir, "static")
    
    
    from_path = os.path.join(root_dir, "content", "index.md")
    template_path = os.path.join(os.path.dirname(__file__), "..", "template.html")
    dest_path = os.path.join(public_dir, "index.html")
    # Step 1: Clear the public directory
    clear_public_directory(public_dir)
    
    # Step 2: Copy static files
    copy_static_files(static_dir, public_dir)
    
    
    
    # Generate the page
    generate_page(
        from_path=from_path,
        template_path=template_path,  # This is in root directory
        dest_path=dest_path)
    print(f"Paths:")
    print(f"- Root: {root_dir}")
    print(f"- Public: {public_dir}")
    print(f"- Static: {static_dir}")
    print("DEBUG Paths:")
    print(f"Does template file exist? {os.path.exists(template_path)}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"from_path: {from_path}")
    print(f"template_path: {template_path}")
    print(f"dest_path: {dest_path}")   
        
    


if __name__ == "__main__":
    main()