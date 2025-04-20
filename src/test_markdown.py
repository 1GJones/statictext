import unittest
import tempfile
import os
from markdown_extractor import TextNode, TextType ,extract_markdown_images ,extract_markdown_links
from main import extract_title,generate_page
    
    
class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
    # Test standard case with one image
        matches = extract_markdown_images(
        "This is text with a single image ![example](https://example.com/image.png)"
    )
        self.assertListEqual([("example", "https://example.com/image.png")], matches)

    # Test multiple images
        matches = extract_markdown_images(
        "![one](https://one.com) and ![two](https://two.com)"
    )
        self.assertListEqual(
        [("one", "https://one.com"), ("two", "https://two.com")],
        matches,
    )

    # Test no images
        matches = extract_markdown_images("This text has no images at all.")
        self.assertListEqual([], matches)

    # Test malformed markdown
        matches = extract_markdown_images("[not closed(https://example.com)")
        self.assertListEqual([], matches)

    
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    # Test multiple links
        matches = extract_markdown_links(
        "[text](https://www.boot.dev) and [text](https://www.youtube.com/@bootdotdev)"
    )
        self.assertListEqual(
        [("text", "https://www.boot.dev"), ("text", "https://www.youtube.com/@bootdotdev")],
        matches,
    )

    # Test no links
        matches = extract_markdown_links("This text has no links at all.")
        self.assertListEqual([], matches)
        
    # Test malformed markdown_links
        matches = extract_markdown_links("[not closed(https://www.boot.dev)")
        self.assertListEqual([], matches)
        
        
class TestExtractTitle(unittest.TestCase):

    def test_basic_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_title_with_extra_spaces(self):
        markdown = "#     Welcome to Boot.dev     "
        self.assertEqual(extract_title(markdown), "Welcome to Boot.dev")

    def test_title_with_additional_content(self):
        markdown = """
## Subtitle
Some text here

# Main Title

Another paragraph
"""
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_title_not_at_top(self):
        markdown = """
Random intro text

# Actual Title

Some paragraph here
"""
        self.assertEqual(extract_title(markdown), "Actual Title")

    def test_raises_if_no_h1(self):
        markdown = """
## This is a subtitle
### Another smaller heading
Some paragraph
"""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_ignores_multiple_hashes(self):
        markdown = """
### Not a title
## Also not a title
# Valid Title
"""
        self.assertEqual(extract_title(markdown), "Valid Title")
        
        
class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        # Set up a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.temp_path = self.test_dir.name

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_generates_expected_html(self):
        # Sample markdown content
        markdown_content = "# Hello Title\n\nThis is **bold** text."
        template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        expected_output = "<html><head><title>Hello Title</title></head><body><div><h1>Hello Title</h1><p>This is <b>bold</b> text.</p></div></body></html>"

        # Create mock markdown and template files
        md_path = os.path.join(self.temp_path, "test.md")
        template_path = os.path.join(self.temp_path, "template.html")
        dest_path = os.path.join(self.temp_path, "output.html")

        with open(md_path, "w") as f:
            f.write(markdown_content)

        with open(template_path, "w") as f:
            f.write(template_content)

        # Run the function
        generate_page(md_path, template_path, dest_path)

        # Read output and verify
        with open(dest_path, "r") as f:
            result = f.read().strip()

        self.assertEqual(result, expected_output)

    def test_missing_h1_raises(self):
        markdown_content = "No headings here"
        template_content = "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>"

        md_path = os.path.join(self.temp_path, "missing_h1.md")
        template_path = os.path.join(self.temp_path, "template.html")
        dest_path = os.path.join(self.temp_path, "output.html")

        with open(md_path, "w") as f:
            f.write(markdown_content)

        with open(template_path, "w") as f:
            f.write(template_content)

        with self.assertRaises(ValueError):
            generate_page(md_path, template_path, dest_path)



if __name__ == "__main__":
    unittest.main()
        
        

