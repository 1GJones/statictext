import unittest
from utilities.shared_nodes import TextType,TextNode
from split_nodes_delimiter import split_nodes_delimiter, split_nodes_image,split_nodes_link

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_code_delimiter(self):
        input_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        input_node = TextNode("This is text with a **bold phrase** here", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input_node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        input_node = TextNode("Some _italic_ text", TextType.TEXT)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([input_node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        input_node = TextNode("Just plain text", TextType.TEXT)
        expected = [input_node]
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        input_node = TextNode("An `unclosed code block", TextType.TEXT)
        expected = [input_node]
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        input_node = TextNode("Some other text", TextType.BOLD)
        expected = [input_node]
        result = split_nodes_delimiter([input_node], "**", TextType.BOLD)
        self.assertEqual(result, expected)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
     )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
        
    def test_no_images(self):
        node = TextNode("This has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
        
    def test_image_at_start(self):
        node = TextNode("![start](http://img.com/start.png) begins here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            
            [
                TextNode("start", TextType.IMAGE, "http://img.com/start.png"),
                TextNode(" begins here", TextType.TEXT),
            ],
            new_nodes,
        )
            
    def test_image_at_end(self):
        node = TextNode("The end has an image ![end](http://img.com/end.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("The end has an image ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "http://img.com/end.png"),
            ],
            new_nodes,
        )
          
    def test_only_image(self):
        node = TextNode("![solo](http://img.com/solo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo", TextType.IMAGE, "http://img.com/solo.png")],
            new_nodes,
        ) 
        
    def test_empty_alt_text(self):
        node = TextNode("Here's an image with no alt text ![](http://img.com/empty.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here's an image with no alt text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "http://img.com/empty.png"),
            ],
            new_nodes,
        ) 
        
    def test_malformed_image_missing_url(self):
        node = TextNode("Broken ![alt]( and more text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_non_text_node(self):
        node = TextNode("![won't touch this](http://img.com/ignore.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_adjacent_images(self):
        node = TextNode("![img1](http://img.com/1.png)![img2](http://img.com/2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "http://img.com/1.png"),
                TextNode("img2", TextType.IMAGE, "http://img.com/2.png"),
            ],
            new_nodes,
        )
        
    def test_single_link(self):
        node = TextNode("Check this [link](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            result,
        )

    def test_multiple_links(self):
        node = TextNode("First [link1](http://a.com) and [link2](http://b.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "http://a.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "http://b.com"),
            ],
            result,
        )

    def test_link_at_start(self):
        node = TextNode("[start](http://start.com) then text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "http://start.com"),
                TextNode(" then text", TextType.TEXT),
            ],
            result,
        )

    def test_link_at_end(self):
        node = TextNode("End with [link](http://end.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("End with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://end.com"),
            ],
            result,
        )

    def test_adjacent_links(self):
        node = TextNode("[one](http://1.com)[two](http://2.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "http://1.com"),
                TextNode("two", TextType.LINK, "http://2.com"),
            ],
            result,
        )

    def test_link_with_empty_text(self):
        node = TextNode("Click this [empty]()", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_malformed_link(self):
        node = TextNode("Oops [broken](", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_non_text_node(self):
        node = TextNode("[skip](http://skip.com)", TextType.BOLD)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_no_links(self):
        node = TextNode("Plain text only", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)


        

if __name__ == '__main__':
    unittest.main()