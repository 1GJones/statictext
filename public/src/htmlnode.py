class HTMLNode:
        def __init__(self, tag=None, value=None, children=None, props=None):
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
            value_repr = f"'{self.value}'" if self.value != '' else "''"
            return f"HTMLNode(tag={tag_repr}, value={value_repr}, children={len(self.children)}, props={self.props_to_html()})"

        
        