import unittest
import sys
import os

# Add the 'src' directory to the system path so 'ParentNode' can be found
sys.path.append(os.path.dirname(__file__))
from html import ParentNode, LeafNode

class TestParentNodeComplex(unittest.TestCase):
    def test_empty_children(self):
        # Test when ParentNode is created with no children
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_multiple_children(self):
        # Test with multiple children under one parent
        node = ParentNode("p", [
            LeafNode(None, "This is the first sentence. "),
            LeafNode(None, "This is the second sentence.")
        ])
        expected_output = "<p>This is the first sentence. This is the second sentence.</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_deep_nesting(self):
        # Test with deep nesting of nodes
        node = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
                ParentNode("li", [LeafNode(None, "Item 3")])
            ])
        ])
        expected_output = "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        self.assertEqual(node.to_html(), expected_output)

    def test_mixed_content(self):
        # Test a mix of LeafNodes and ParentNodes
        node = ParentNode("p", [
            LeafNode(None, "Here is some text followed by a list: "),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")])
            ]),
            LeafNode(None, " And now we're back to text.")
        ])
        expected_output = "<p>Here is some text followed by a list: <ul><li>Item 1</li><li>Item 2</li></ul> And now we're back to text.</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_no_props_empty_string(self):
        # Test ParentNode with no props and an empty string
        node = ParentNode("span", [LeafNode(None, "")])
        expected_output = "<span></span>"
        self.assertEqual(node.to_html(), expected_output)

    def test_no_children(self):
        # Test if ParentNode has no children at all
        node = ParentNode("div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_incorrect_nesting(self):
        # Test a case of mismatched tags, like <ul> having text instead of <li>
        node = ParentNode("ul", [LeafNode(None, "This should be an <li> element")])
        expected_output = "<ul>This should be an <li> element</ul>"
        self.assertEqual(node.to_html(), expected_output)

if __name__ == "__main__":
    unittest.main()
