import unittest

from src.markdown_to_html_node import block_to_block_type
class TestBlockToBlockType(unittest.TestCase):
     
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("## Subheading"), "heading")
    
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), "code")
        self.assertEqual(block_to_block_type("``` python\nprint('Hello')\n```"), "code")
    
    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), "quote")
        self.assertEqual(block_to_block_type("> First line\n> Second line"), "quote")
    
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), "unordered_list")
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), "ordered_list")
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), "ordered_list")
    
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), "paragraph")
        self.assertEqual(block_to_block_type("Some text."), "paragraph")
    
    def test_ordered_list_invalid_sequence(self):
        # Numbers are not sequential, so it should be treated as a paragraph
        self.assertEqual(block_to_block_type("1. First item\n3. Third item"), "paragraph")

if __name__ == '__main__':
    unittest.main()
