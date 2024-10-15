import sys
import os
import unittest

# Add the 'src' directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from textnode import TextNode
from leafnode import LeafNode
from leafnode import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    # Define text types as constants
    text_type_text = "text"
    text_type_code = "code"
    text_type_bold = "bold"
    text_type_link = "link"

    def test_different_delimiter(self):
        node = TextNode("Text with [bold] parts", self.text_type_text)
        new_nodes = split_nodes_delimiter([node], "[", self.text_type_bold)
        
        expected_nodes = [
            TextNode("Text with ", self.text_type_text, None),
            TextNode("bold", self.text_type_bold, None),
            TextNode("] parts", self.text_type_text, None)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_no_text_between_delimiters(self):
        node = TextNode("Text with `` empty delimiter", self.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", self.text_type_code)
        
        expected_nodes = [
            TextNode("Text with ", self.text_type_text, None),
            TextNode("", self.text_type_code, None),
            TextNode(" empty delimiter", self.text_type_text, None)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_non_text_node(self):
        node = TextNode("This is a link", self.text_type_link, url="https://example.com")
        new_nodes = split_nodes_delimiter([node], "`", self.text_type_code)
        
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_single_delimiter(self):
        node = TextNode("This is text with a `code block` word", self.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", self.text_type_code)
        
        expected_nodes = [
            TextNode("This is text with a ", self.text_type_text, None),
            TextNode("code block", self.text_type_code, None),
            TextNode(" word", self.text_type_text, None)
        ]
        self.assertEqual(new_nodes, expected_nodes)        

    def test_multiple_delimiters(self):
        node = TextNode("This is text with a `code block` and another `code block`", self.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", self.text_type_code)
        
        expected_nodes = [
            TextNode("This is text with a ", self.text_type_text, None),
            TextNode("code block", self.text_type_code, None),
            TextNode(" and another ", self.text_type_text, None),
            TextNode("code block", self.text_type_code, None)
        ]
        self.assertEqual(new_nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
