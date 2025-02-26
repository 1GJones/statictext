import unittest
from src.extract_title import extract_title  # Adjust the import if necessary
from textwrap import dedent
class TestMarkdownFunctions(unittest.TestCase):

    def test_extract_title_valid(self):
        """Test extracting a valid h1 title."""
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_leading_trailing_spaces(self):
        """Test extracting a title with leading/trailing spaces around it."""
        markdown = "#    Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_multiline_markdown(self):
        """Test extracting a title from a multi-line markdown."""
        markdown = dedent( """
        # This is the title

        Some content below the title.
        """)
        self.assertEqual(extract_title(markdown), "This is the title")

    def test_extract_title_no_h1(self):
        """Test the function raises an exception if no h1 header exists."""
        markdown = """
        ## No h1 header here

        Some content below.
        """
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("No h1 title found in the markdown content" in str(context.exception))

    def test_extract_title_empty_input(self):
        """Test the function raises an exception for empty markdown input."""
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("No h1 title found in the markdown content" in str(context.exception))

if __name__ == '__main__':
    unittest.main()

