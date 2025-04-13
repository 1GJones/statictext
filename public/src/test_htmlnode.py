import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestHtMLNode(unittest.TestCase):
    
    def test_default_initialazation(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, '')
        self.assertEqual(len(node.children), 0)
        self.assertEqual(node.props,{})
        self.assertEqual(repr(node), "HTMLNode(tag=None, value='', children=0, props=)")

    def test_initialization_with_props(self):
        node=HTMLNode(props={"class": "primary"})
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, '')
        self.assertEqual(len(node.children), 0)
        self.assertEqual(node.props, {"class": "primary"})
        self.assertEqual(repr(node), 'HTMLNode(tag=None, value=\'\', children=0, props=class="primary")')
        
    def test_initilization_with_children(self):
        child1 = HTMLNode(tag='p', value='Child 1')
        child2 = HTMLNode(tag='p',value='Child 2')
        node = HTMLNode(children=[child1,child2])
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, '')
        self.assertEqual(len(node.children), 2)
        self.assertEqual(repr(node), "HTMLNode(tag=None, value='', children=2, props=)")
            
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
        
    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_leaf_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")
        
    
    def test_leaf_with_attributes(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>') 
        
        
    def test_parent_tag(self):
        node=ParentNode(tag=None, children=[HTMLNode(tag='span', value='Child')])
        with self.assertRaises(ValueError) as context:
            if not context:
                raise ValueError("ParentNode must have a tag.")
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag.")
        
    def test_parent_without_tag(self):
        node= ParentNode(None, [HTMLNode('span', 'Child')])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag.")
        
    def test_parent_have_children(self):
        node=ParentNode(tag='div', children=[])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children.")
        

    def test_parent_without_children(self):
        node=ParentNode('div', [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children.")
        

        
if __name__ == '__main__':
    unittest.main()