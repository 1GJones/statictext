import unittest
from src.textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_code_delimiter(self):
        input_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        input_node = TextNode("This is text with a **bold phrase** here", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input_node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        input_node = TextNode("Some _italic_ text", TextType.TEXT)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input_node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        input_node = TextNode("Just plain text", TextType.TEXT)
        expected = [input_node]
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        input_node = TextNode("An `unclosed code block", TextType.TEXT)
        expected = [input_node]
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        input_node = TextNode("Some other text", TextType.BOLD)
        expected = [input_node]
        result = split_nodes_delimiter([input_node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()