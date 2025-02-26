import unittest

from src.splitnode_image import split_nodes_image # type: ignore
from src.split_node_delimiter import split_nodes_link
from textnode import TextNode

class TestSplitNodesFunctions(unittest.TestCase):
    
    def test_split_nodes_link_single_link(self):
        node = TextNode(
            "Here is a link [to Google](https://www.google.com)", 
            "text"
        )
        result = split_nodes_link([node])
        
        expected = [
            TextNode("Here is a link ", "text"),
            TextNode("to Google", "link", "https://www.google.com")
        ]
        
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            "Links: [Google](https://www.google.com), [GitHub](https://github.com).",
            "text"
        )
        result = split_nodes_link([node])
        
        expected = [
            TextNode("Links: ", "text"),
            TextNode("Google", "link", "https://www.google.com"),
            TextNode(", ", "text"),
            TextNode("GitHub", "link", "https://github.com"),
            TextNode(".", "text")
        ]
        
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is plain text without any links.", "text")
        result = split_nodes_link([node])
        
        expected = [TextNode("This is plain text without any links.", "text")]
        
        self.assertEqual(result, expected)

    def test_split_nodes_image_single_image(self):
        node = TextNode(
            "Here is an image: ![Image](https://example.com/image.png)", 
            "text"
        )
        result = split_nodes_image([node])
        
        expected = [
            TextNode("Here is an image: ", "text"),
            TextNode("Image", "image", "https://example.com/image.png")
        ]
        
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_images(self):
        node = TextNode(
            "Images: ![Img1](https://example.com/img1.png) and ![Img2](https://example.com/img2.png).",
            "text"
        )
        result = split_nodes_image([node])
        
        expected = [
            TextNode("Images: ", "text"),
            TextNode("Img1", "image", "https://example.com/img1.png"),
            TextNode(" and ", "text"),
            TextNode("Img2", "image", "https://example.com/img2.png"),
            TextNode(".", "text")
        ]
        
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is plain text without any images.", "text")
        result = split_nodes_image([node])
        
        expected = [TextNode("This is plain text without any images.", "text")]
        
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
