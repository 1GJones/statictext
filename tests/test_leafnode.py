import sys
import os
import unittest

# Append the correct path to sys.path so that statictext can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.htmlnode import LeafNode  # Correct import

class TestLeafNode(unittest.TestCase):
    def test_render_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected_output = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_render_link(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        expected_output = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_output)

    def test_render_raw_text(self):
        node = LeafNode(None, "This should be raw text.")
        expected_output = "This should be raw text."
        self.assertEqual(node.to_html(), expected_output)

    def test_value_required(self):
        with self.assertRaises(ValueError):
             LeafNode("p")  # Missing value should raise ValueError

if __name__ == "__main__":
    unittest.main()
