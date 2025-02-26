import sys
import os
import re

# Adjust the system path to include the directory containing htmlnode.py
from htmlnode import HTMLNode,LeafNode
from textnode import TextNode


def text_to_children(text):
    
    """
    Converts a string into a list of child nodes with inline formatting.
    Args:
        text (str): The input text to be parsed.

    Returns:
        list: A list of HTMLNode and LeafNode objects representing the text with formatting.

    """
    print(f"Processing text: '{text}'")  # Debug
    nodes = []
    patterns = {
        'b': r'\*\*(.*?)\*\*',  # Bold
        'i': r'\*(.*?)\*',      # Italic
        'code': r'`(.*?)`',     # Inline code
        'a': r'\[(.*?)\]\((.*?)\)'  # Links

    }
    
    pos = 0

    while pos < len(text):
        match = None
        early_match = len(text)
        matched_tag = None
        
        for tag,pattern in patterns.items():
        # Append any plain text before the match
             current_match = re.search(pattern,text[pos:])
             if current_match and current_match.start() < early_match:
                 match = current_match
                 early_match = current_match.start()
                 matched_tag = tag
                 
                 
        if match:
            # Handle text before match
           if match.start() > 0:
              nodes.append(TextNode(text[pos:pos + match.start()], text_type= "text"))
            
            # Handle the match itself 
              
           if matched_tag =='b':
               nodes.append(HTMLNode(tag='b', children=[TextNode(text=match.group(1), text_type="text")]))
               print(f"Found bold text: {match.group(1)}")   
           elif matched_tag =='i':
                nodes.append(HTMLNode(tag ='i', children=[TextNode(text=match.group(1), text_type= "text")]))
                print(f"Found italic text: {match.group(1)}")
           elif matched_tag == 'code':
                nodes.append(HTMLNode(tag='code',children=[TextNode(text=match.group(1), text_type="text")]))
           
           elif matched_tag == 'a':
               nodes.append(HTMLNode(tag='a', children=[TextNode(text=match.group(1), text_type="text")],props={"href": match.group(2)}))

            
            #Append the formated text as an HTMLNode
        
           pos += match.start() + len(match.group(0))
        else:      
      
        # No more matches, add remaining text
            nodes.append(LeafNode(value=text[pos:]))
            break   
            
    return nodes