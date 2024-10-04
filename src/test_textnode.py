import sys
import os

# Add the 'src' directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from textnode import TextNode
import unittest


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


if __name__ == "__main__":
    unittest.main()

