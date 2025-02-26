import sys
import os
import shutil
from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node



def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from markdown and template files.

    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template
        dest_path (str): Path where the final HTML should be saved.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    print("DEBUG Paths:")
    print(f"Does template file exist? {os.path.exists(template_path)}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"from_path: {from_path}")
    print(f"template_path: {template_path}")
    print(f"dest_path: {dest_path}")
    template_path = os.path.join(os.path.dirname(__file__), "..", "template.html")
    
    # Step 1: Read markdown from
    
    try:
        with open(from_path, 'r', encoding='utf-8') as file:
            markdown_from = file.read()
    except FileNotFoundError:
        print(f"Markdown file not found: {from_path}")
        return
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        return

    
    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template = template_file.read()
            print("DEBUG: Raw template:", repr(template))
            print("DEBUG: Template bytes:", [ord(c) for c in template[:100]])
            print("DEBUG: Template contains '{{ Title }}'?", "{{ Title }}" in template)
            print("DEBUG: Template contains '{{ Content }}'?", "{{ Content }}" in template)
            print("DEBUG: Template exact contents:")
            print("---START OF TEMPLATE---")
            print(template)
            print("---END OF TEMPLATE---")
            print("Length of template:", len(template))

    except FileNotFoundError:
        print(f"DEBUG: Template file exists? {os.path.exists(template_path)}")
        print(f"Template file not found: {template_path}")
        return
    except Exception as e:
        print("DEBUG Template contents:", template[:100])
        print(f"Error reading template file: {e}")
        return
    

    # Step 2: Extract the title from the markdown
    try:
        page_title = extract_title(markdown_from)
        print("DEBUG: Extracted title:", repr(page_title))
    except Exception as e:
        print(f"Error extracting title: {e}")
        return

    # Step 3: Convert the markdown from to HTML
    try:
        html_node = markdown_to_html_node(markdown_from)
        if html_node is None:
            raise ValueError("markdown_to_html_node returned None")
        html_from = html_node.to_html()
        print("DEBUG: First 100 chars of HTML:", html_from[:100]) 
    except Exception as e:
        print(f"Error converting markdown to HTML: {e}")
        return

    # Step 5: Validate the template has placeholders
    
    if "{{ Title }}" not in template or "{{ Content }}" not in template:
        print("DEBUG Template contents:", template[:100])  # first 100 chars
        raise ValueError("Template is missing required placeholders")  # Step 6: Replace placeholders in the template
    filled_html = template.replace("{{ Title }}", page_title)
    filled_html = filled_html.replace("{{ Content }}", html_from)
    print("DEBUG: Filled template contains '{{ Title }}'?", "{{ Title }}" in filled_html)
    print("DEBUG: Filled template contains '{{ Content }}'?", "{{ Content }}" in filled_html)

    # Step 7: Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    print(f"[DEBUG] dest_path is:{dest_path}")
    # Step 8: Write the final HTML to the destination file
    try:
        with open(dest_path, 'w', encoding='utf-8') as output_file:
            output_file.write(filled_html)
        print(f"Generated page saved at {dest_path}")
    except Exception as e:
        print(f"Error writing to destination file: {e}")
        return




