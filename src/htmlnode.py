import sys
import os
import re
# Adjust the system path to include the directory containing htmlnode.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src' )))
from textnode import TextNode
class HTMLNode:
   
   
    def __init__(self, tag="", value=None, children=None, props=None):
        self.tag = tag
        self.value = value if value is not None else ""
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
        
    def props_to_html(self):
        """Convert properties (props) into a HTML string for attributes."""
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items ())
        
    def to_html(self):
        """Recursively convert the node and its children to HTML."""
        # If no tag, just return children's HTML
        if not self.tag:
            return ''.join([child.to_html() if hasattr(child, 'to_html') else str(child) for child in self.children])
    
        props_html =  f' {self.props_to_html()}' if self.props else ''
        children_html = ''.join([child.to_html() if hasattr(child, 'to_html') else str(child) for child in self.children])
        if self.tag == 'code': 
            return f"<{self.tag}{props_html}>{self.value}{children_html}</{self.tag}>"
        return f"<{self.tag}{props_html}>{self.value}{children_html}</{self.tag}>"

    def __repr__(self):
        if self.value :
            return f"<{self.tag}>{self.value}</{self.tag}>" if self.tag else self.value
        return f"<{self.tag}></{self.tag}>"


class LeafNode:
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode requires value")  # Raise ValueError if no value is provided
        self.tag = tag
        self.value = value # Use value for text, not value
        self.props = props or {}
        
    def __eq__(self, other):
        if isinstance(other, LeafNode):
            return self.tag == other.tag and self.value == other.value
        return False
    
    def to_html(self):
        if not self.tag:
            return self.value
        
        if self.tag == "img":
            # Handle missing src and alt
            src = self.props.get("src", "#")  # Default to "#" if src is missing
            alt = self.props.get("alt", "")   # Default to empty alt text
            return f'<img src="{src}" alt="{alt}"/>'
        
        props_str = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    

    
    def __repr__(self):
        props_str = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        if self.tag:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return self.value



def split_nodes_delimiter(old_nodes, delimiter, new_text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == "text":  # Process only text nodes
            parts = node.text.split(delimiter) if node.text else []

            if len(parts) == 1:  # No delimiter found, add node as-is
                new_nodes.append(node)
                continue

            # Split based on delimiter and assign correct types
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # Add the part as normal text (for text outside delimiters)
                    if part:
                        new_nodes.append(TextNode(part, "text", None))
                else:
                    # Handle the case where the closing `]` is part of the text
                    if "]" in part:
                        inside_delimiter, after_delimiter = part.split("]", 1)
                        new_nodes.append(TextNode(inside_delimiter.strip(), new_text_type, None))
                        if after_delimiter:
                            new_nodes.append(TextNode("]" + after_delimiter, "text", None))
                    else:
                        # Add the part with the new text type
                        new_nodes.append(TextNode(part.strip(), new_text_type, None))

        else:
            # If the node is not of type 'text', just add it as is
            new_nodes.append(node)  # Ensure non-text nodes are appended to new_nodes

    return new_nodes
