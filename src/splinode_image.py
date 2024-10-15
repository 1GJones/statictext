import re

from textnode import TextNode

def split_nodes_image(old_nodes):
    new_nodes = []
    
    # Regular expression to match images in the format ![alt](URL)
    image_pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    
    for node in old_nodes:
        content = node.content
        last_pos = 0
        
        # Iterate over all matches for images
        for match in re.finditer(image_pattern, content):
            start, end = match.span()
            
            # Append the text before the image as a new TextNode
            if last_pos < start:
                new_nodes.append(TextNode(content[last_pos:start], node.text_type))
            
            # Extract the alt text and URL, and create a TextNode for the image
            alt_text, url = match.groups()
            new_nodes.append(TextNode(alt_text, "image", url))
            
            last_pos = end
        
        # Add remaining text after the last image
        if last_pos < len(content):
            new_nodes.append(TextNode(content[last_pos:], node.text_type))
    
    return new_nodes if new_nodes else [node]