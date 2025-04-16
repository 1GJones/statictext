class HTMLNode:
    def __init__(self, tag=None, value='', children=None, props=None):
        """
        Base HTML node with optional tag, value, children, and props.
        """
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html().")

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        self.props = self.props_to_html().lstrip()
        return f"HTMLNode(tag={self.tag}, value='{self.value}', children={len(self.children)}, props={self.props})" 
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        
        """
        Initializes a LeafNode with a required tag and value, and optional properties.

        :param tag: A string representing the HTML tag name (e.g., "p", "a", "h1").
        :param value: A string representing the inner text of the HTML tag.
        :param props: A dictionary containing attributes of the HTML tag.
        """
        
        super().__init__(tag=tag, value=value, children=[], props=props)
        
    
    def to_html(self):
        """
        Renders the leaf node as an HTML string.
        
        :return: A string representing the HTML of the leaf node.
        :raises ValueError: If the leaf node has no value.
        """
        
        if self.tag is None:
            return self.value
        
        props_str = self.props_to_html()
        
        # Self-closing for void elements like <img>
        if self.tag in ["img", "br", "hr", "input", "meta", "link"]:
            return f"<{self.tag}{props_str} />"
        
        if not self.value:
            raise ValueError("LeafNode must have a value.")

        
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    
    
    def __init__(self, tag, children, props=None):
        """
        Initializes a ParentNode with a required tag and children, and optional properties.

        :param tag: A string representing the HTML tag name (e.g., "div", "ul").
        :param children: A list of HTMLNode objects representing child elements.
        :param props: A dictionary containing attributes of the HTML tag.
        """
        super().__init__(tag=tag, value='', children=children, props=props)
    
        
        
    
    def to_html(self):
        """
        Renders the parent node and its children as an HTML string.

        :return: A string representing the HTML of the parent node and its children.
        :raises ValueError: If the parent node has no tag or children.
        """
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        if not self.children:
            raise ValueError("ParentNode must have children.")

        props_str = self.props_to_html()
        children_html = ''.join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"