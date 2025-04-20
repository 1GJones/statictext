from textnode_to_html import text_node_to_html_node
from utilities.shared_nodes import TextType
from block_to_block_type import block_to_block_type, BlockType
from text_to_textnodes import text_to_textnodes, TextNode
from textnode_to_html import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode # assuming your HTML node class is here
import re


def split_markdown_blocks(markdown):
    lines = markdown.strip().splitlines()
    blocks = []
    current_block = []
    in_code_block = False
    
    for line in lines:
        strip = line.strip()
        
        if strip.startswith("```"):
           if not in_code_block and current_block:
              blocks.append("\n".join(current_block))
              current_block = []
           in_code_block = not in_code_block
           current_block.append(line)

           continue
        
        if not in_code_block and strip == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)
            
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks

def markdown_to_html_node(markdown: str, wrap_in_div=True):
    blocks = split_markdown_blocks(markdown)
    block_nodes = []
    
    
    
    for block in blocks:
        block = block.strip()
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            count = block.count("#", 0, block.find(" ")) # Count # before first space
            heading_text = " ".join(block[count+1:].splitlines()).strip()
            children = text_node_to_html_node(text_to_textnodes(heading_text))
            block_nodes.append(ParentNode(tag=f"h{count}", children = children))
            
        elif block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(line.strip() for line in block.splitlines()).strip()
            children = text_node_to_html_node(text_to_textnodes(paragraph_text)) 
            block_nodes.append(ParentNode(tag="p", children=children))
            
        elif block_type == BlockType.CODE:
            code_content = block
            if block.startswith("```") and block.endswith("```"):
               code_content = "\n".join(block.splitlines()[1:-1])
            code_text_node = TextNode(code_content, text_type=TextType.CODE)
            code_html = text_node_to_html_node([code_text_node])[0]
            block_nodes.append(ParentNode(tag="pre", children=[code_html]))

        elif block_type == BlockType.QUOTE:
            quote_lines = [line[2:] for line in block.splitlines() if line.startswith("> ")]
            quote_text = " ".join(quote_lines)
            children = text_node_to_html_node(text_to_textnodes(quote_text)) 
            block_nodes.append(ParentNode(tag="blockquote", children=children))


        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.splitlines()
            list_nodes = [ParentNode(tag="li", children=text_node_to_html_node(text_to_textnodes(re.sub(r"^[-*+]\s+", "", item.strip())))) for item in list_items]
            block_nodes.append(ParentNode(tag="ul", children=list_nodes))
            
        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.splitlines()
            list_nodes = [ParentNode(tag="li", children=text_node_to_html_node(text_to_textnodes(re.sub(r"^\d+\.\s+", "", item.strip())))) for item in list_items]
            block_nodes.append(ParentNode(tag="ol", children=list_nodes))
          #wrap everything in a top-level <div>
                
    if wrap_in_div:
        return ParentNode(tag="div", children=block_nodes)
    elif len(block_nodes)==1:
        return block_nodes[0] # avoid extra <div>
    else:
        return ParentNode(tag="div", children= block_nodes)
