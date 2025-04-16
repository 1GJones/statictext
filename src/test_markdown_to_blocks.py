import unittest
from markdown_to_blocks import markdown_to_blocks
from utilities.shared_nodes import TextType,TextNode

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_single_block(self):
        md = "This is a single block."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block."])

    def test_multiple_empty_lines(self):
        md = """
        
Block 1

Block 2

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])
    
    def test_windows_newlines(self):
         md = "Block 1\r\n\r\nBlock 2\r\n"
         blocks = markdown_to_blocks(md)
         self.assertEqual(blocks, ["Block 1", "Block 2"])
    
    def test_mixed_newlines(self):
        md = "Block 1\n\r\nBlock 2\r\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])
    
    def test_blank_lines_in_block(self):
         md = """Block 1
        
        line2

        Block 2"""
         blocks = markdown_to_blocks(md)
         self.assertEqual(blocks, ['Block 1\n        \n        line2', 'Block 2'])
 
if __name__ == '__main__':
    unittest.main()