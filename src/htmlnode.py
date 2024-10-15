import sys
import os
import html
import re

# Adjust the system path to include the directory containing htmlnode.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src' )))

class HTMLNode:
    def __init__(self, tag="", value="",children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props if props else {}

    def __repr__(self):
        if self.value:       
         return f"<{self.tag}>{self.value}</{self.tag}>" if self.tag else self.value

    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value")  # Raise ValueError if no value is provided
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def __repr__(self):
        if self.tag:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return self.value     

def text_to_children(text):
    nodes=[]
    
    bold_pattern = r'\*\*(.*?)\*\*' # **bold**
    italic_pattern =r'\*(.*?)\*' # *italic*
    
# Use a single pattern to handle both bold and italic
    seguay_pattern = re.compile(f'({bold_pattern}|{italic_pattern})')    
# First, split the text by both bold and italic patterns
    last_pos = 0
    
    # Iterate through the matches of combined patterns
    for match in re.finditer(seguay_pattern, text):
        start, end = match.span()

        # Add the text before the match as regular text
        if last_pos < start:
            nodes.append(HTMLNode(value=text[last_pos:start]))

        # Check if the match is bold
        bold_match = re.match(bold_pattern, match.group(0))
        if bold_match:
            nodes.append(HTMLNode(tag='b', value=bold_match.group(1)))

        # Check if the match is italic
        italic_match = re.match(italic_pattern, match.group(0))
        if italic_match:
            nodes.append(HTMLNode(tag='i', value=italic_match.group(1)))

        # Update last_pos to the end of the current match
        last_pos = end

    # Add any remaining text after the last match as regular text
    if last_pos < len(text):
        nodes.append(HTMLNode(value=text[last_pos:]))

    return nodes
