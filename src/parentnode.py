import sys
import os
import re

from htmlnode import HTMLNode
from leafnode import LeafNode
from text_to_children import text_to_children
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

class ParentNode(HTMLNode):
    def __init__(self, tag,  children=None, props=None):
        super().__init__(tag, value="", children = children, props=props)
    

    def to_html(self):
        if not self.children:
            raise ValueError("ParentNode must have at least one child")
        """Generate the HTML representation, ensuring value is included before children."""
        props_html = f' {self.props_to_html()}' if self.props else ''
        children_html = ''.join([child.to_html() for child in self.children])
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"