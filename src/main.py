import os
import shutil
import sys
from markdown_to_html_node import markdown_to_html_node
from textnode import TextNode, TextType

def extract_title(markdown):
    """
    Extract the first H1 (# Heading) from the markdown text.
    The H1 must start with exactly one '#' followed by a space.
    """
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown.")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if not file.endswith(".md"):
                continue

            # Full path to markdown file
            from_path = os.path.join(root, file)

            # Path relative to content dir
            rel_path = os.path.relpath(from_path, dir_path_content)

            # Change extension from .md → .html
            rel_html_path = os.path.splitext(rel_path)[0] + ".html"

            # Full path for output
            dest_path = os.path.join(dest_dir_path, rel_html_path)

            # Generate HTML page
            generate_page(from_path, template_path, dest_path)



def generate_page(from_path, template_path, dest_path, basepath ="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path,'r') as f:
        markdown_content = f.read()
        
        #Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
        
        # convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Remove the outer div tags
    if html_content.startswith("<div>") and html_content.endswith("</div>"):
        html_content = html_content[5:-6]  # strip "<div>" and "</div>"
        
        
        # Extracct the title
    title = extract_title(markdown_content)
        
        # Replace placeholders in the template
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)
    
    # Basepath replacements
    full_html = full_html.replace('href="/', f'href="{basepath}/')
    full_html = full_html.replace('src="/', f'src="{basepath}/')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)   
        # Create destination directory if it doesnt exist
            
    with open(dest_path, 'w') as f:
        f.write(full_html)
    print(f"✅ Page written to {dest_path}")
    
       

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

    for root, _, files in os.walk(static_dir):
        rel_path = os.path.relpath(root, static_dir)
        dest_dir = os.path.join(public_dir, rel_path)
        os.makedirs(dest_dir, exist_ok=True)
        
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy(src, dst)
            print(f"✅ Copied: {src} → {dst}")

    print(f"\n📦 Static content successfully copied to: {public_dir}")
    
    


def main():
    # Get basepath from command-line
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"🌐 Using base path: {basepath}")
    
    copy_static_to_public()
    
    # Generate index.html from content
    template_path = "template.html"
    generate_pages_recursive("content", template_path, "public")


if __name__ == "__main__":
    main()

