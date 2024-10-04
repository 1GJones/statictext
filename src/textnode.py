import sys
import os

# Adjust the system path to include the parent directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from htmlnode import LeafNode


class TextNode:
    def __init__(self, content, text_type, url=None):
        self.content = content
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            isinstance(other, TextNode) and
            self.content == other.content and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.content}, {self.text_type}, {self.url})" 
    
    
    
# Mapping from text node types to corresponding HTML tags
def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(value=text_node.content)
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.content)
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.content)
    elif text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.content)
    elif text_node.text_type == "link":
        if not text_node.url:
            raise ValueError("Link type TextNode requires a URL.")
        return LeafNode(tag="a", value=text_node.content, props={"href": text_node.url})
    elif text_node.text_type == "image":
        if not text_node.url:
           raise ValueError("Image type TextNode requires a URL.")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.content})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")


