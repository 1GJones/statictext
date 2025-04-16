import re 
from enum import Enum

class TextType(Enum):
    
    """Enum representing different types of text nodes."""
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    """Class representing a text node with content, type, and an optional URL."""

    
    def __init__(self, text: str, text_type: TextType, url: str = None):
        """
        Initializes a TextNode.

        Args:
            text (str): The text content of the node.
            text_type (TextType): The type of text (e.g., NORMAL, BOLD, LINK, etc.).
            url (str, optional): The URL for links or images. Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url 
        
    def __eq__(self,other):
        """Returns True if all properties of two TextNode objects are equal."""
        if not isinstance(other,TextNode):
            return False 
        return (self.text == other.text and 
                self.text_type == other.text_type and
                self.url == other.url)
        
    def __repr__(self):
        """Returns a string representation of the TextNode."""
        return f"TextNode(text=({self.text!r},{self.text_type},{self.url!r})"
    
    
    
    
if __name__ == "__main__":
    node1 = TextNode("Hello", TextType.TEXT)
    node2 = TextNode("Hello", TextType.TEXT)
    node3 = TextNode("Different", TextType.TEXT)
    node4 = TextNode("Hello", TextType.LINK, "https://example.com")

