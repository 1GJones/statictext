import re

from textnode import TextNode

def split_nodes_link(old_nodes):
    new_nodes = []
    
    # Regular expression to match links in the format [anchor](URL)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    for node in old_nodes:
        content = node.content
        last_pos = 0
        
        # Iterate over all matches for links
        for match in re.finditer(link_pattern, content):
            start, end = match.span()
            
            # Append the text before the link as a new TextNode
            if last_pos < start:
                new_nodes.append(TextNode(content[last_pos:start], node.text_type))
            
            # Extract the link and create a TextNode for the link
            anchor, url = match.groups()
            new_nodes.append(TextNode(anchor, "link", url))
            
            # Update last_pos to the end of the current match
            last_pos = end
        
        # Add remaining text after the last link (if any)
        if last_pos < len(content):
            new_nodes.append(TextNode(content[last_pos:], node.text_type))
    
    # If no links were found, return the original node
    return new_nodes if new_nodes else [node]
