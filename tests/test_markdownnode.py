import unittest
import re
import os
import sys

from src.htmlnode import HTMLNode,LeafNode
from src.markdown_to_html_node import markdown_to_blocks, markdown_to_html_node,parse_nested_list

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Function to extract markdown links
def extract_markdown_links(text):
    # Define the regex pattern to capture markdown link syntax
    pattern = r'\[([^\]]*)\]\(([^)]*)\)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Return a list of tuples (anchor_text, url)
    return matches
def print_node_tree(node, level=0):
    indent = "  " * level
    print(f"{indent}<{node.tag}>: {getattr(node, 'value', '')}")
    for child in node.children:
        if isinstance(child, HTMLNode):
            print_node_tree(child, level + 1)
        else:
            print(f"{indent}  Leaf: {child}")


# Test class for markdown link extraction
class TestMarkdownExtraction(unittest.TestCase):
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_output = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected_output)
    
    def test_no_links(self):
        text = "This text has no links."
        expected_output = []
        self.assertEqual(extract_markdown_links(text), expected_output)
        
    def test_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com) and [StackOverflow](https://stackoverflow.com)"
        expected_output = [("Google", "https://google.com"), ("GitHub", "https://github.com"), ("StackOverflow", "https://stackoverflow.com")]
        self.assertEqual(extract_markdown_links(text), expected_output)
    
    def test_empty_anchor_text(self):
        text = "Link with no text [](https://www.emptytext.com)"
        expected_output = [("", "https://www.emptytext.com")]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_empty_url(self):
        text = "Link with empty URL [empty]()"
        expected_output = [("empty", "")]
        self.assertEqual(extract_markdown_links(text), expected_output)
        
        
class TestMarkdowntoBlocks(unittest.TestCase):
    def test_simple_markdown(self):
        markdown = """
        # Heading
        
        This is a paragraph.
        
        * List item 1
        * List item 2
        """
        expected = [
            "# Heading",
            "This is a paragraph.",
            "* List item 1\n* List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_nested_lists(self):
        markdown = """
        * Item 1
          * Subitem 1
          * Subitem 2
        * Item 2
        """
        expected = [
            "* Item 1\n * Subitem 1\n  * Subitem 2",
            "* Item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_trailing_whitespace(self):
        markdown = "   # Heading   \n\n   This is a paragraph.  \n\n   "
        expected = [
            "# Heading",
            "This is a paragraph."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_no_blocks(self):
        markdown = "\n\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)
        
class TestMarkdownToHtmlNode(unittest.TestCase):
    
    def test_heading(self):
        markdown = "# Heading 1"
        result = markdown_to_html_node(markdown)
        print(f"Result: {result}")
        self.assertEqual(result.tag, 'div')
        self.assertEqual(result.children[0].tag, 'h1')
        self.assertEqual(result.children[0].children[0].value, 'Heading 1')
    
    def test_paragraph(self):
        markdown = "This is a paragraph with **bold** and *italic* text."
        result = markdown_to_html_node(markdown)
    
    # Ensure the root is a div
        self.assertEqual(result.tag, 'div')
    
    # Ensure the first child is a paragraph
        self.assertEqual(result.children[0].tag, 'p')
        self.assertEqual(result.children[0].children[0].value, 'This is a paragraph with ')

    # Now check the children of the paragraph for bold and italic text
        paragraph_children = result.children[0].children
    
        self.assertEqual(paragraph_children[1].tag, 'b')  # This should be bold
        self.assertEqual(paragraph_children[1].children[0].value, 'bold')
        self.assertEqual(paragraph_children[2].value, ' and ')  # Regular text
        self.assertEqual(paragraph_children[3].tag, 'i')  # This should be italic
        self.assertEqual(paragraph_children[3].children[0].value, 'italic')
        self.assertEqual(paragraph_children[4].value, ' text.')  # Regular text
    
    def test_code_block(self):
        markdown = "```\nCode block\n```"
        result = markdown_to_html_node(markdown)
        print(result.children)
        
        self.assertEqual(result.tag, 'div')
        self.assertEqual(result.children[0].tag, 'pre')
        
        code_node = result.children[0].children[0]
        self.assertEqual(code_node.tag, 'code')
        self.assertEqual(code_node.value.strip(), 'Code block')
    

    
    def test_unordered_list(self):
        markdown = "* Item 1\n* Item 2"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, 'div')
        self.assertEqual(result.children[0].tag, 'ul')
        self.assertEqual(result.children[0].children[0].tag, 'li')
        self.assertEqual(result.children[0].children[0].children[0].value, 'Item 1')
        self.assertEqual(result.children[0].children[1].children[0].value, 'Item 2')
    
    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item"
        result = markdown_to_html_node(markdown)
        print(result)
        self.assertEqual(result.tag, 'div')
        self.assertEqual(result.children[0].tag, 'ol')
        self.assertEqual(result.children[0].children[0].tag, 'li')
        self.assertEqual(result.children[0].children[0].children[0].value, 'First item')
        self.assertEqual(result.children[0].children[0].tag, 'li')
        self.assertEqual(result.children[0].children[1].children[0].value, 'Second item')
        
    def test_simple_list(self):
         markdown = """
         * Item 1
         * Item 2
         """
         result = parse_nested_list(markdown, list_type="ul")
         self.assertEqual(result.tag, 'ul')
         self.assertEqual(len(result.children), 2)
         self.assertEqual(result.children[0].children[0].value, 'Item 1')
         self.assertEqual(result.children[1].children[0].value, 'Item 2')


        

if __name__ == '__main__':
    unittest.main()
