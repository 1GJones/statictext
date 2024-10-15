import sys
import os
import re

from htmlnode import HTMLNode, text_to_children

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src' )))


def markdown_to_html_node(markdown):
    # 1. Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # 2. Create the root HTMLNode
    root = HTMLNode(tag='div') #This is the parent HTMLNode that will contain all block elements
    
    # 3. Loop over each block
    for block in blocks:
        block_type = block_to_block_type(block) #Determine block type
        
        if block_type == "heading":
            heading_level = block.count('#',0,block.find(' ')) # Count # characters before the space
            block_content = block[heading_level + 1:].strip() # Get the text after the # symbols
            heading_node = HTMLNode(tag=f'h{heading_level}', children=text_to_children(block_content))
            root.children.append(heading_node)
            
        elif block_type == "paragraph":
            paragraph_node = HTMLNode(tag='p',children=text_to_children(block))
            root.children.append(paragraph_node)
            
        elif block_type == "code":
            code_content = block.strip('```').strip()
            code_node = HTMLNode(tag='pre', children=[HTMLNode(tag="code", value=code_content)])
            root.children.append(code_node)
            
        elif block_type == "quote":
            # Remove leading '>' from each line in the block and handle as text
            quote_lines = [line[1:].strip()for line in block.splitlines()]
            quote_text = ' '.join(quote_lines)
            quote_node = HTMLNode(tag='blockquote', children=text_to_children(quote_text))
            root.children.append(quote_node)
            
            
        elif block_type == "unordered_list":
            list_node = HTMLNode(tag="ul")
            for line in block.splitlines():
                list_item_content = line[2:].strip() # Strip "* " or "- " from the start
                list_node.children.append(HTMLNode(tag="li", children=text_to_children(list_item_content)))
            root.children.append(list_node)
            
        elif block_type == "ordered_list":
            list_node = HTMLNode(tag="ol")
            for line in block.splitlines():
                list_item_content = line[line.find('. ') +2:].strip() # Strip "1. "  from the start
                list_node.children.append(HTMLNode(tag="li", children=text_to_children(list_item_content)))
            root.children.append(list_node)
            
    return root
def markdown_to_blocks(markdown):
    
    raw_blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    return blocks

    
    

def block_to_block_type(block):
    # Check for heading: starts with 1-6 # followed by a space
    if block.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
        return "heading"
# Check for code block: starts and ends with three backticks
    if block.startswith('```') and block.endswith('```'):
        return "code"
    
    # Check for quote block: every line starts with '>'
    if all(line.startswith('>') for line in block.splitlines()):
        return "quote"
    
    # Check for unordered list: every line starts with '*' or '-'
    if all(line.startswith(('* ', '- ')) for line in block.splitlines()):
        return "unordered_list"
    
    # Check for ordered list: every line starts with a number followed by ". "
    lines = block.splitlines()
    if all(line.strip().split(". ", 1)[0].isdigit() and line.strip().split(". ", 1)[1] for line in lines):
        # Ensure the numbers are sequential starting from 1
        for i, line in enumerate(lines, start=1):
            number = int(line.strip().split(". ", 1)[0])
            if number != i:
                return "paragraph"  # If numbers are not sequential, it's a paragraph
        return "ordered_list"
    
    # If none of the above conditions are met, it's a paragraph
    return "paragraph" 

