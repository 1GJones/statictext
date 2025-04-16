import unittest

from block_to_block_type import BlockType, block_to_block_type
class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Subheading"), BlockType.HEADING)

    def test_code_block_triple_backticks(self):
        self.assertEqual(block_to_block_type("```python\nprint('hi')\n```"), BlockType.CODE)

    def test_code_block_indented(self):
        self.assertEqual(block_to_block_type("    def func():\n        pass"), BlockType.CODE)
        self.assertEqual(block_to_block_type("\tdef func():\n\t\tpass"), BlockType.CODE)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item one"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("* Another item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("+ Last item"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("42. The answer"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("No special markdown here."), BlockType.PARAGRAPH)

    def test_heading_with_no_space(self):
        # Not a valid heading, should be paragraph
        self.assertEqual(block_to_block_type("##Invalid"), BlockType.PARAGRAPH)

    def test_unordered_list_with_no_space(self):
        # Should default to paragraph
        self.assertEqual(block_to_block_type("-NoSpace"), BlockType.PARAGRAPH)

    def test_ordered_list_with_no_dot(self):
        self.assertEqual(block_to_block_type("1 First item"), BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()
