import sys
import os
import re

from htmlnode import HTMLNode,LeafNode
from text_to_children import text_to_children

def markdown_to_html_node(markdown):
    if not isinstance(markdown, str) or not markdown.strip():
        return []
    blocks = markdown_to_blocks(markdown)
    nodes = []
    root=HTMLNode(tag="", children=nodes)
    

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            block_head = block.count('#', 0, block.find(' '))
            content = block[block_head:].strip()
            nodes.append(HTMLNode(tag=f'h{block_head}', children=[LeafNode(value=content)]))

        elif block_type == "paragraph":
             paragraph_node = HTMLNode(tag='p')
             paragraph_node.children = text_to_children(block)
             nodes.append(paragraph_node)

        elif block_type in {"unordered_list", "ordered_list"}:
            # Determine list tag (ul or ol)
            list_tag = "ul" if block_type == "unordered_list" else "ol"
            list_node = HTMLNode(tag=list_tag)  # Create the list node
            nodes.append(parse_nested_list(block, list_node))  # Append the list node to the root


        elif block_type == "code":
            lines = block.splitlines()
    # Skip the opening ``` line and closing ``` line
            print("Debug - Code block content before processing:")
            print(repr(block))
            code_content = "\n".join(lines[1:-1])
            print("Debug - Final code content:")
            print(repr(code_content))
            code_node = HTMLNode(tag='code', children=[LeafNode(value=code_content)])
            pre_node = HTMLNode(tag='pre', children=[code_node])
            nodes.append(pre_node)

        elif block_type == "quote":
            quote_text = " ".join(line.lstrip('> ') for line in block.splitlines())
            nodes.append(HTMLNode(tag='blockquote', children=text_to_children(quote_text)))

        print(f"Processing block: {block}, Block type: {block_type}")
    return root


def markdown_to_blocks(markdown):
     """
    Splits markdown text into logical blocks for processing.

    Args:
    markdown (str): The raw markdown string.

    Returns:
        list: A list of blocks where each block is a string.
    """
     blocks = []
     current_block = []
     in_code_block = False

     for line in markdown.split('\n'):
         if line.startswith('```'):
             # Toggle the in_code_block flag
             current_block.append(line)
             if in_code_block:
                # If we're closing a code block, add it to blocks
                
                #Join the lines in the curren_block with newlines
                blocks.append("\n".join(current_block))
               # Reset current_block to empty
                current_block = []
             in_code_block = not in_code_block 
            
         elif in_code_block:
                # If inside a code block, just append lines as-is
                current_block.append(line)
         elif line.strip() == "" and current_block:
              blocks.append("\n".join(current_block))
              current_block = []
         elif line.strip() != "":
            current_block.append(line)
               
     if current_block: 
        blocks.append("\n".join(current_block))
        current_block = []
             
                   
     return blocks 
           
    
    



def get_indentation_level(line):
         """
         Returns the number of leading spaces in a line.
         """
         expand_line = line.replace("\t", "    ")
         return len(expand_line) - len(expand_line.lstrip())


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
    if all(line.lstrip().startswith(('* ', '- ')) for line in block.splitlines()):
        return "unordered_list"
    # Check for ordered list: every line starts with a number followed by ". "
    if all(re.match(r'^\d+\.\s+', line) for line in block.splitlines()):
        return "ordered_list"
    # Default to paragraph if none of the above

    return "paragraph"

def parse_list_item(lines, current_indent):
    """
    Parse individual list items into a nested structure based on indentation.
    """
    blocks = []
    child_lines = []
    child_indent = None
    
 

    for line in lines:
        indent = get_indentation_level(line)

        # If the indentation increases, start collecting child lines
        if indent >= current_indent:
            if child_indent is None:
                child_indent = indent
            if indent == child_indent:
                child_lines.append(line)
            else:
                blocks.append(parse_list_item(child_lines, child_indent))
                child_lines = [line]
                child_indent = indent
        elif indent == current_indent:
            if child_lines:
                blocks.append(parse_list_item(child_lines, child_indent))
                child_lines = []
            blocks.append(line.strip())
        else:
            if child_lines:
                blocks.append(parse_list_item(child_lines, child_indent))
            break
        # Append any remaining child lines
    if child_lines:
        blocks.append(parse_list_item(child_lines, child_indent))
    return blocks

def parse_nested_list(block, list_node):
    lines = block.splitlines()

    for line in lines:
        if not line.strip():
            continue
        
        
        # Remove list markers and get content
        content = line.strip()
        if list_node.tag == 'ol':
            #Remove "1. " or "2. " etc 
            content = re.sub(r'^\d+\.\s+', '', content)
        
        else:
        # Remove "* " or "- "
            content = re.sub(r'^[-*]\s+', '', content)

        li_node = HTMLNode(tag='li', children=text_to_children(content))
        list_node.children.append(li_node)
    
    return list_node