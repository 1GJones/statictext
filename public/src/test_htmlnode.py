import unittest

from htmlnode import HTMLNode

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

        
if __name__ == '__main__':
    unittest.main()