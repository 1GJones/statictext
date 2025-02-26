import re

from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        
        # Splitting logic: Find matching delimiters
        split_text = node.text.split(delimiter)
        
        if len(split_text) % 2 == 0:
            raise ValueError("Mismatched delimiters in text.")

        for i, part in enumerate(split_text):
            if part:  # Avoid empty strings from split
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, "text"))
                else:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes
 