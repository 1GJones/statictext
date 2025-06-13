
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


# Grab the basepath argument or default to "/"
base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

# Define the output directory for GitHub Pages
output_dir = "docs"

# Make sure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
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
            generate_page(from_path, template_path, dest_path, basepath)



def generate_page(from_path, template_path, dest_path, basepath ="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path,'r') as f:
        markdown_content = f.read()
        
        #Read the template file
    with open(template_path, 'r') as f:
        temp_content = f.read()
        full_html = temp_content
        # convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    print("🔧 HTML content:", html_content)
    
    # Remove the outer div tags
    # if html_content.startswith("<div>") and html_content.endswith("</div>"):
    #     html_content = html_content[5:-6]  # strip "<div>" and "</div>"
        
        
        # Extract the title
    title = extract_title(markdown_content)
    
        # Replace placeholders in the template
    full_html = full_html.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)
    
    basepath_clean = basepath.rstrip("/")
    if basepath_clean == "":
        basepath_clean = "."

    full_html = full_html.replace("{{ BasePath }}", basepath_clean)
    
   # Only apply href/src rewrite if basepath is not "."
    if basepath_clean == ".":
        full_html = full_html.replace('href="/', 'href="./')
        full_html = full_html.replace('src="/', 'src="./')
    else:
        full_html = full_html.replace('href="/', f'href="{basepath_clean}/')
        full_html = full_html.replace('src="/', f'src="{basepath_clean}/')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)   
     # Create destination directory if it doesnt exist            
    with open(dest_path, 'w') as f:
        f.write(full_html)
    print(f"✅ Page written to {dest_path}")
    
       

def copy_static_to_dir(static_dir,output_dir):
    project_root = os.getcwd()
    static_dir = os.path.join(project_root, static_dir)
    output_dir = os.path.join(project_root, output_dir)

    if not os.path.exists(static_dir):
        print(f"❌ Source directory '{static_dir}' does not exist.")
        return

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"🧹 Removed existing '{output_dir}'")

    os.mkdir(output_dir)
    print(f"📁 Created: {output_dir}")

    for root, dirs, files in os.walk(static_dir):
        rel_path = os.path.relpath(root, static_dir)
        dest_dir = os.path.join(output_dir, rel_path)
        os.makedirs(dest_dir, exist_ok=True)
        if "docs" in dirs:
            dirs.remove("docs")
        
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy(src, dst)
            print(f"✅ Copied: {src} → {dst}")

    print(f"\n📦 Static content successfully copied to: {output_dir}")
    
    


def main():
    # Get basepath from command-line
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    basepath = basepath.rstrip("/")
    print(f"🌐 Using base path: {basepath}")
    # Generate index.html from content
    template_path = "template.html"

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "public"
  # ✅ updated from public → docs
    copy_static_to_dir("static", output_dir)
    
    generate_pages_recursive("content", template_path, output_dir,basepath)


if __name__ == "__main__":
    main()
