import sys
import os

# Add the 'src' directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


from src.textnode import TextNode 
from src.htmlnode import LeafNode

from text_node_to_html_node import text_node_to_html_node, text_to_textnodes
import unittest

# Define text types as constants
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TestTextNodeToHtml(unittest.TestCase):

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
        expected_output = '<img src="image.png" alt="Alt text"/>'
        self.assertEqual(html_node.to_html(), expected_output)

    def test_invalid_text_type(self):
        text_node = TextNode("Unknown", "unknown_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_create_text_node(self):
        # Test basic TextNode creation
        node = TextNode("This is a text node", text_type_text)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, text_type_text)
        self.assertIsNone(node.url)
    
    def test_text_node_equality(self):
        # Test TextNode equality based on content, text_type, and URL
        node1 = TextNode("Same content", text_type_text)
        node2 = TextNode("Same content", text_type_text)
        self.assertEqual(node1, node2)
        
        node3 = TextNode("Different content", text_type_text)
        self.assertNotEqual(node1, node3)
        
        node4 = TextNode("Same content", text_type_link, "https://example.com")
        node5 = TextNode("Same content", text_type_link, "https://example.com")
        self.assertEqual(node4, node5)
    
    def test_text_to_textnodes(self):
        # Test the conversion of a string into multiple TextNodes
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ]
        self.assertEqual(nodes, expected)
    
    def test_html_node_conversion(self):
        # Test the conversion of TextNodes to HTML nodes
        node_text = TextNode("This is text", text_type_text)
        node_bold = TextNode("Bold text", text_type_bold)
        node_link = TextNode("Link text", text_type_link, "https://example.com")
        node_image = TextNode("Image alt text", text_type_image, "https://example.com/image.jpg")
        
        html_node_text = text_node_to_html_node(node_text)
        self.assertEqual(html_node_text.value, "This is text")
        
        html_node_bold = text_node_to_html_node(node_bold)
        self.assertEqual(html_node_bold.tag, "b")
        self.assertEqual(html_node_bold.value, "Bold text")
        
        html_node_link = text_node_to_html_node(node_link)
        self.assertEqual(html_node_link.tag, "a")
        self.assertEqual(html_node_link.value, "Link text")
        self.assertEqual(html_node_link.props["href"], "https://example.com")
        
        html_node_image = text_node_to_html_node(node_image)
        self.assertEqual(html_node_image.tag, "img")
        self.assertEqual(html_node_image.props["src"], "https://example.com/image.jpg")
        self.assertEqual(html_node_image.props["alt"], "Image alt text")
    
    def test_empty_content(self):
        # Test how the functions behave with empty content
        node = TextNode("", text_type_text)
        self.assertEqual(node.text_type, text_type_text)
        self.assertEqual(node.text,"")
        
        # Test text_to_textnodes with empty content
        empty_nodes = text_node_to_html_node( node)
        self.assertEqual(empty_nodes, [])
    
    def test_no_links_in_text(self):
        # Test text with no links
        node = TextNode("This is plain text with no links.", text_type_text)
        result = text_node_to_html_node(node).to_html()
        expected = "This is plain text with no links."
        self.assertEqual(result, expected)
    
    def test_no_images_in_text(self):
        # Test text with no images
        node = TextNode("This is plain text with no images.", text_type_text)
        result = text_node_to_html_node(node).to_html()
        expected = "This is plain text with no images."
        self.assertEqual(result, expected)
    
    def test_image_with_no_url(self):
        # Test TextNode with an image type but no URL, should raise ValueError
        with self.assertRaises(ValueError):
            node = TextNode("Image without URL", text_type_image)
            text_node_to_html_node(node)
            

if __name__ == "__main__":
    unittest.main()
