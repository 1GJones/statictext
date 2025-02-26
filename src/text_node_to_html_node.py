import sys
import os
import re


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.htmlnode import HTMLNode, LeafNode
from src.textnode import TextNode,text_type_text,text_type_bold,text_type_italic,text_type_code,text_type_image,text_type_link

# Mapping from TextNode types to HTMLNode (LeafNode)
def text_node_to_html_node(text_node):
    if not isinstance(text_node,TextNode):
        raise TypeError("Expected a TextNode instance")
    if text_node.text_type not in [text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image]:
        raise ValueError("Invalid text type")
    if text_node.text.strip() == "":  # Ensure empty input returns an empty list
        return []

    if text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == text_type_bold:
         return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == text_type_italic:
         return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == text_type_link:
         if not text_node.url:
            raise ValueError("Link type TextNode requires a URL.")
         return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == text_type_image:
            if not text_node.url:
                raise ValueError("Image type TextNode requires a URL.")
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})


def text_to_textnodes(text):
    nodes = []
    remaining_text = text

    # Find italic text (single asterisks)
    patterns = [
        (r'\*\*(.*?)\*\*', text_type_bold),        # Bold: **text**
        (r'\*(.*?)\*', text_type_italic),          # Italic: *text*
        (r'`(.*?)`', text_type_code),              # Code: `text`
        (r'\[(.*?)\]\((.*?)\)', text_type_link),   # Link: [text](url)
        (r'!\[(.*?)\]\((.*?)\)', text_type_image)  # Image: ![text](url)
    ]
    
    while remaining_text:
        earliest_match = None
        match_pattern = None
# Find the earliest matching pattern
        for pattern, node_type in patterns:
            match = re.search(pattern, remaining_text)
            if match and (earliest_match is None or match.start() < earliest_match.start()):
                earliest_match = match
                match_pattern = node_type
        
        if earliest_match:
            start = earliest_match.start()
            
            # Add any text before the match
            if start > 0:
                nodes.append(TextNode(remaining_text[:start], text_type_text))
            
            # Handle the matched pattern
            if match_pattern in (text_type_link, text_type_image):
                text_content = earliest_match.group(1)
                url = earliest_match.group(2)
                nodes.append(TextNode(text_content, match_pattern, url))
                
                    
            else:
                nodes.append(TextNode(earliest_match.group(1), match_pattern))
            
            remaining_text  = remaining_text[earliest_match.end():] 
        else:
            if remaining_text.strip():
                nodes.append(TextNode(remaining_text, text_type_text)) 
    # Convert TextNodes to HTMLNodes
    return nodes

