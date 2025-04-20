import unittest
import textwrap
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = textwrap.dedent("""\
        ```
        print("Code")
        ```
         """)  
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
        html,
        "<div><pre><code>print(\"Code\")</code></pre></div>"
    )
        
        
    def test_heading(self):
        md = "# This is a Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a Heading</h1></div>"
        )

    def test_blockquote(self):
        md = "> This is a quote\n> continued on next line"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote continued on next line</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- First item\n- Second item\n- Third **bold** item"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third <b>bold</b> item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item with `code`\n3. Third"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third</li></ol></div>"
        )

    def test_mixed_blocks(self):
        md = """# Title

        This is a paragraph with a [link](https://example.com)

    > A quote

    - List item one
    - List item two

    """
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph with a <a href=\"https://example.com\">link</a></p><blockquote>A quote</blockquote><ul><li>List item one</li><li>List item two</li></ul></div>"
            
        )


if __name__ == "__main__":
    unittest.main()
