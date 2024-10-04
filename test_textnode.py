import sys
import os

# Add the 'src' directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from textnode import TextNode 
from leafnode import LeafNode
from htmlnode import text_node_to_html_node
import unittest

# Define text types as constants
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TestTextNode(unittest.TestCase):

    # Test if two nodes with the same properties are equal
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    # Test if two nodes with different text types are not equal
    def test_neq_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    # Test if two nodes with different URLs are not equal
    def test_neq_url(self):
        node = TextNode("This is a text node", "bold", "https://example.com")
        node2 = TextNode("This is a text node", "bold", "https://another.com")
        self.assertNotEqual(node, node2)

    # Test default value of url (should be None)
    def test_default_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)

    # Test string representation of the node
    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://example.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, https://example.com)")
        
    def test_text_node(self):
        text_node = TextNode("Hello, World!", text_type_text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Hello, World!")

    def test_bold_text_node(self):
        text_node = TextNode("Bold Text", text_type_bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold Text</b>")

    def test_image_node(self):
        text_node = TextNode("Alt text", text_type_image, url="image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="image.png" alt="Alt text"/>')

    def test_invalid_text_type(self):
        text_node = TextNode("Unknown", "unknown_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)



if __name__ == "__main__":
    unittest.main()
