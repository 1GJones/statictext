import unittest
import os
import sys
import tempfile
import shutil

from main import  main  
class TestCopyStaticToPublic(unittest.TestCase):

    def setUp(self):
        # Create a temporary project root
        self.test_dir = tempfile.TemporaryDirectory()
        self.project_root = self.test_dir.name

        # Set up fake static directory
        self.static_dir = os.path.join(self.project_root, 'static')
        os.mkdir(self.static_dir)

        # Add test files and nested directory
        with open(os.path.join(self.static_dir, 'index.html'), 'w') as f:
            f.write("<html>Hello</html>")

        os.mkdir(os.path.join(self.static_dir, 'assets'))
        with open(os.path.join(self.static_dir, 'assets', 'style.css'), 'w') as f:
            f.write("body { color: red; }")

        # Change working directory to test project root
        self.original_cwd = os.getcwd()
        os.chdir(self.project_root)

    def tearDown(self):
        # Restore original working directory
        os.chdir(self.original_cwd)
        # Cleanup
        self.test_dir.cleanup()

    def test_copy_static_to_public(self):
        # Simulate command-line args
        sys.argv = ["main.py", "/", "public"]

        # Run the function
        main()

        # Check if public directory and its contents exist
        public_dir = os.path.join(self.project_root, 'public')
        self.assertTrue(os.path.exists(public_dir))
        self.assertTrue(os.path.exists(os.path.join(public_dir, 'index.html')))
        self.assertTrue(os.path.exists(os.path.join(public_dir, 'assets', 'style.css')))

        # Check file content
        with open(os.path.join(public_dir, 'index.html')) as f:
            self.assertEqual(f.read(), "<html>Hello</html>")

        with open(os.path.join(public_dir, 'assets', 'style.css')) as f:
            self.assertEqual(f.read(), "body { color: red; }")

if __name__ == '__main__':
    unittest.main()
