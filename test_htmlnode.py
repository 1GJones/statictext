import unittest
import sys
import os

# Adjust system path to include the parent directory of 'src'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import HTMLNode from htmlnode.py and LeafNode from leafnode.py
from htmlnode import HTMLNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        node = HTMLNode("a", "Click me!", props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph.")
        expected_output = "<p>This is a paragraph.</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_parent_node_with_children(self):
        child1 = HTMLNode("span", "Child 1")
        child2 = HTMLNode("span", "Child 2")
        parent = ParentNode("div", "Parent content: ", children=[child1, child2])
        expected_output = "<div>Parent content: <span>Child 1</span><span>Child 2</span></div>"
        self.assertEqual(parent.to_html(), expected_output)

if __name__ == "__main__":
    unittest.main()
