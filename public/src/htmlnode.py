class HTMLNode:
    def __init__(self, tag=None, value='', children=None, props=None):
            """
        Initializes an HTMLNode with optional tag, value, children, and properties.
        
        :param tag: A string representing the HTML tag name (e.g., "p", "a", "h1").
        :param value: A string representing the inner text of the HTML tag.
        :param children: A list of HTMLNode objects representing child elements.
        :param props: A dictionary containing attributes of the HTML tag.
        """ 
            self.tag = tag
            self.value = value 
            self.children = children if children is not None else []
            self.props = props if props is not None else {}
        
         
    def to_html(self):
            """Raises NotImplemetedError. Child classes will override this method."""
            raise NotImplementedError("to_html method must be implemented by subclasses")
        
    def props_to_html(self):
            """Returns a string representation of the htML attributes."""
            return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items()) if self.props else ""
        
    def __repr__(self):
            """Provides a detailed string representation of an HTMLNode for debugging."""
            tag_repr = f"'{self.tag}'" if self.tag is not None else 'None'
            value_repr = f"'{self.value}'" if {self.value} else "'"
            # For props, we want to avoid the leading space in the representation
            props_str = self.props_to_html().lstrip() 
            return f"HTMLNode(tag={tag_repr}, value={value_repr}, children={len(self.children)}, props={props_str})"
        

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
        if not self.value:
            raise ValueError("LeafNode must have a value.")
        
        if not self.tag:
            return self.value
        
        props_str = self.props_to_html()
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