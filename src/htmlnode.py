import sys
import os
import html


# Adjust the system path to include the directory containing htmlnode.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src' )))

class HTMLNode:
    def __init__(self, tag="", value="", props=None):
        self.tag = tag
        self.value = value
        self.props = props if props else {}

    def __repr__(self):
        props_string = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        return f"<{self.tag} {props_string}>{self.value}</{self.tag}>" if self.tag else self.value


class LeafNode(HTMLNode):
    def __init__(self, tag="", value="", props=None):
        value = html.escape(self.value)

        super().__init__(tag, value, props)


