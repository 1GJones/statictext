import unittest
from src.extract_title import extract_title  # Update import as per your file structure

class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        markdown= "#  Hello\nSome content."
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_no_title(self):
        markdown= "No h1 header here"
        with self.assertRaises(ValueError):
            extract_title((markdown))
    
    def test_multiline(self):
        markdown = "Some text\n# Title\nOther text"
        self.assertEqual(extract_title(markdown), "Title")
    
    def test_trailing_spaces(self):
        self.assertEqual(extract_title("#    Hello World    "), "Hello World")
        
    def test_multiple_hashes(self):
        with self.assertRaises(ValueError):
             extract_title("## Not an h1")
             
    def test_empty_string(self):
        with self.assertRaises(ValueError) as context:
            extract_title("")
        self.assertTrue("No h1 title found in the markdown content" in str(context.exception))  # Ensure case matches  
    def test_no_space_after_hash(self):
        with self.assertRaises(ValueError):
            extract_title("#NoSpace")

if __name__ == "__main__":
    unittest.main()
