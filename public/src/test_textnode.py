import unittest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from text_to_textnodes import text_to_textnodes
from utilities.shared_nodes import TextType,TextNode
from markdown_extractor import extract_markdown_images,extract_markdown_links


class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        """Test equality when two TextNode objects have identical properties."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        """Test inequality when the text peoperty is different."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text", TextType.BOLD)
        self.assertNotEqual(node,node2)
        
    def test_not_eq_different_text_type(self):
        """Test inequality when the text_type property is different."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
        
    def test_eq_with_default_url(self):
        """Test equality when both objects have a default None URL."""
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_not_eq_different_url(self):
        """Test inequality when the URL property is different."""
        node1 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node1, node2)

    def test_basic_formatting(self):
        text = "This is **bold**, _italic_, and `code`."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "Image here ![cat](http://img.com/cat.png) and more."
        expected = [
            TextNode("Image here ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "http://img.com/cat.png"),
            TextNode(" and more.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "Visit [Boot.dev](https://boot.dev) for courses."
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" for courses.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_combined_formatting(self):
        text = "Text with **bold**, _italic_, `code`, [link](http://x.com), and ![img](http://img.com)."
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://x.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "http://img.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_malformed_markdown(self):
        text = "This is **bold with no end and _italic."
        expected = [TextNode(text, TextType.TEXT)]  # No valid formatting — treat as plain
        self.assertEqual(text_to_textnodes(text), expected)

    def test_adjacent_elements(self):
        text = "**bold**_italic_`code`"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_text(self):
        text = ""
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()