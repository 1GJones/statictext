from htmlnode import LeafNode
from utilities.shared_nodes import TextType

def text_node_to_html_node(text_nodes):
    html_nodes = []

    for text_node in text_nodes:
        text = text_node.text
        node_type = text_node.text_type

        if node_type == TextType.TEXT:
            html_nodes.append(LeafNode(tag=None, value=text))

        elif node_type == TextType.BOLD:
            html_nodes.append(LeafNode(tag="b", value=text))

        elif node_type == TextType.ITALIC:
            html_nodes.append(LeafNode(tag="i", value=text))

        elif node_type == TextType.CODE:
            html_nodes.append(LeafNode(tag="code", value=text))

        elif node_type == TextType.LINK:
            html_nodes.append(LeafNode(tag="a", value=text, props={"href": text_node.url}))

        elif node_type == TextType.IMAGE:
            html_nodes.append(LeafNode(tag="img", value="", props={
                "src": text_node.url,
                "alt": text
            }))

        else:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")

    return html_nodes
