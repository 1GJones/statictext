import unittest
import re
import os
import sys

from src.markdown_to_html_node import get_indentation_level, markdown_to_html_node,parse_nested_list

class TestIndentation(unittest.TestCase):
    def test_no_indentation(self):
        """Line with no leading spaces should return 0."""
        self.assertEqual(get_indentation_level("NoIndentation"), 0)

    def test_single_space(self):
        """Line with a single leading space should return 1."""
        self.assertEqual(get_indentation_level(" SingleSpace"), 1)

    def test_multiple_spaces(self):
        """Line with multiple leading spaces should return the correct count."""
        self.assertEqual(get_indentation_level("   MultipleSpaces"), 3)

    def test_tab_indentation(self):
        """Tabs should be ignored in this function (not expanded to spaces)."""
        self.assertEqual(get_indentation_level("\tTabIndented"), 0)

    def test_mixed_spaces_and_tabs(self):
        """Mixed spaces and tabs should only count leading spaces."""
        self.assertEqual(get_indentation_level(" \tMixedSpacesAndTabs"), 1)

    def test_empty_line(self):
        """Empty lines should return 0."""
        self.assertEqual(get_indentation_level(""), 0)

    def test_whitespace_only_line(self):
        """Line with only spaces should return the count of those spaces."""
        self.assertEqual(get_indentation_level("     "), 5)
        
        
    def test_mixed_indentation(self):
        markdown = """
        * Item 1
          * Subitem 1
            * Subsubitem 1
          * Subitem 2
        * Item 2
        """
        result = parse_nested_list(markdown, list_type="ul")
        self.assertEqual(len(result.children), 2)  # Two top-level items

        # Nested structure
        nested_list = result.children[0].children[1]
        sub_nested_list = nested_list.children[0].children[1]
        self.assertEqual(sub_nested_list.children[0].children[0].value, 'Subsubitem 1')




if __name__ == "__main__":
    unittest.main()