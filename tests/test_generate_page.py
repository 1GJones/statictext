import unittest
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.main import generate_page

class TestGeneratePage(unittest.TestCase):

    def setUp(self):
       # Ensure the directory is created before writing the file
        """Initialize directories and setup necessary files."""
        os.makedirs("content", exist_ok=True)
        os.makedirs("public", exist_ok=True)
        
        with open("content/index.md", "w") as f:
            f.write("# Test Title\n\nThis is a test.")

        with open("template.html", "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

    def tearDown(self):
        """Clean up test directories and files."""
        if os.path.exists("content"):
            shutil.rmtree("content")  # Safeguard with ignore_errors
        if os.path.exists("public"):
            shutil.rmtree("public")
        if os.path.exists("template.html"):
            os.remove("template.html")

    def test_generate_page_with_simple_markdown(self):
        """Test the page generation with a simple markdown template."""
        generate_page(from_path="content/index.md", 
                      template_path="template.html", 
                      dest_path="public/index.html")

        # Check if the file was created
        self.assertTrue(os.path.exists("public/index.html"),"The generated HTML file does not exist.")

        # Verify contents of the generated HTML
        with open("public/index.html", "r") as f:
             generated_html = f.read()
             
        self.assertIn("<title>Test Title</title>", generated_html, "The title was not correctly inserted into the template.")
        self.assertIn("<div><h1>Test Title</h1><p>This is a test.</p></div>", generated_html, "The content was not correctly inserted ino the template.")
             
if __name__ == "__main__":
    unittest.main()