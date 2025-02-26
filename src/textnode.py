import sys
import os
import re

# Adjust the system path to include the parent directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# Define text types
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            isinstance(other, TextNode) and
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html(self):
        if self.text_type == "text":
            return self.text
        elif self.text_type == "bold":
            return f"<b>{self.text}</b>"
        elif self.text_type == "italic":
            return f"<i>{self.text}</i>"
        elif self.text_type == "code":
            return f"<code>{self.text}</code>"
        elif self.text_type == "link":
            if not self.url:
                raise ValueError("Link type TextNode requires a URL.")
            return f'<a href="{self.url}">{self.text}</a>'
        elif self.text_type == "image":
            if not self.url:
                raise ValueError("Image type TextNode requires a URL.")
            return f'<img src="{self.url}" alt="{self.text}"/>'
        else:
            raise ValueError(f"Unknown text type: {self.text_type}")


