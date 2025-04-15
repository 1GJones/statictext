import os
import shutil
from src.textnode import TextNode, TextType


def copy_static_to_public():
    project_root = os.getcwd()
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")

    if not os.path.exists(static_dir):
        print(f"❌ Source directory '{static_dir}' does not exist.")
        return

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        print(f"🧹 Removed existing '{public_dir}'")

    os.mkdir(public_dir)
    print(f"📁 Created: {public_dir}")

    for root, dirs, files in os.walk(static_dir):
        rel_path = os.path.relpath(root, static_dir)
        dest_dir = os.path.join(public_dir, rel_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy(src, dst)
            print(f"✅ Copied: {src} → {dst}")

    print(f"\n📦 Static content successfully copied to: {public_dir}")


def main():
    copy_static_to_public()


if __name__ == "__main__":
    main()

    # Temporary debug test (optional)
    # You can delete this later or move to a unit test
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print("🧪 Debug TextNode:", node)
