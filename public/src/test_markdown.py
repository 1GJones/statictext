import unittest


from markdown_extractor import TextNode, TextType ,extract_markdown_images ,extract_markdown_links
    
    
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

if __name__ == "__main__":
    unittest.main()