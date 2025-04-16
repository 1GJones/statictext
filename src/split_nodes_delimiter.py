import re
from utilities.shared_nodes import TextType,TextNode
from markdown_extractor import extract_markdown_images,extract_markdown_links

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
        
        text = node.text
        
        images = extract_markdown_images(text)
        
        if not images:
            image_node.append(node)
            continue
        
        # Process text with image
        remaining_text = text
        
        
        for image_alt, image_url in images:
            # Split text around the current image
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            # Add text before image if not empty
            if parts[0]:
                image_node.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the image node
            image_node.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update remaining text to process
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # Add any remaining text after the last image
        if remaining_text:
           image_node.append(TextNode(remaining_text, TextType.TEXT))
    
    return image_node
        
def split_nodes_link(old_nodes):
    link_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            link_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            link_nodes.append(node)
            continue

        remaining_text = text

        for link_alt, link_url in links:
            if not link_alt.strip() or not link_url.strip():
                continue  # Skip empty alt text or empty url like []()

            markdown_syntax = f"[{link_alt}]({link_url})"
            match_index = remaining_text.find(markdown_syntax)

            if match_index == -1:# Valid case: markdown pattern is found
           # Add text before the matched link
                continue  # Extractor found it, but can't locate in text? Skip it.

            if match_index > 0:
                link_nodes.append(TextNode(remaining_text[:match_index], TextType.TEXT))

            link_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            remaining_text = remaining_text[match_index + len(markdown_syntax):]

        if remaining_text:
            link_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return link_nodes
