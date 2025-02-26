import unittest
import os
import sys

# Ensure 'src' is in the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import TextNode and split_nodes_delimiter
from src.textnode import TextNode
from src.split_node_delimiter import  split_nodes_delimiter 
class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_bold_text(self):
        nodes = [TextNode("Hello **bold** world!", "text")]
        result = split_nodes_delimiter(nodes, "**", "bold")
        expected = [
            TextNode("Hello ", "text"),
            TextNode("bold", "bold"),
            TextNode(" world!", "text"),
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        nodes = [TextNode("This is *italic* text.", "text")]
        result = split_nodes_delimiter(nodes, "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text.", "text"),
        ]
        self.assertEqual(result, expected)

    def test_code_inline(self):
        nodes = [TextNode("Some `code` here.", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = [
            TextNode("Some ", "text"),
            TextNode("code", "code"),
            TextNode(" here.", "text"),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
