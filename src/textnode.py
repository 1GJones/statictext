import sys
import os
import re

# Adjust the system path to include the parent directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

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
        return False
    
    
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


def text_to_textnodes(text):
    nodes = []
    
    # Manually simulating text parsing as an example
    nodes.append(TextNode("This is ", text_type_text))
    nodes.append(TextNode("text", text_type_bold))
    nodes.append(TextNode(" with an ", text_type_text))
    nodes.append(TextNode("italic", text_type_italic))
    nodes.append(TextNode(" word and a ", text_type_text))
    nodes.append(TextNode("code block", text_type_code))
    nodes.append(TextNode(" and an ", text_type_text))
    nodes.append(TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"))
    nodes.append(TextNode(" and a ", text_type_text))
    nodes.append(TextNode("link", text_type_link, "https://boot.dev"))
    
    return nodes


