from split_nodes_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from utilities.shared_nodes import TextType,TextNode
def text_to_textnodes(text):
    # Step 1: Start with one full Text node
    if text == "":
        return [TextNode("", TextType.TEXT)]
    
    nodes = [TextNode(text, TextType.TEXT)]
 
 # Step 2: Split images first 
    nodes = split_nodes_image(nodes)
    
# Step 3: Split links
    nodes = split_nodes_link(nodes)
     
     # Step 4: Apply inline formatting in this order: bold -> italic -> code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)      
 
    return nodes
 
