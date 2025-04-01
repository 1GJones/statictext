import re
from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    

    for node in old_nodes:
        # If node is not of TEXT type, add it as-is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Always add empty text nodes
            
        # Process TEXT nodes
        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            # Unbalanced delimiters — treat whole thing as normal text
            new_nodes.append(node)
            continue

            
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
            
def split_nodes_image(old_nodes):
    
    image_node = []
    
    for node in old_nodes:
        # If node is not of TEXT type, add it as-is
        if node.text_type != TextType.TEXT:
            image_node.append(node)
            continue
        
        curr_text = node.text
        
        images = extract_markdown_images(curr_text)
        
        if not images:
            image_node.append(node)
            continue
        
    