print("Hello, World")
from textnode import TextNode, TextType

def main():
    """Main function to test the TextNode class."""
    node = TextNode("This is a text node", TextType.BOLD, "httos://www.boot.dev")
    print(node)
    
    
if __name__ == "__main__":
    main()