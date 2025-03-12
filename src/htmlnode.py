class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None, parent=None):
        self.tag = tag
        self.value = value
        self.children = children or []  # Ensure children is never None
        self.props = props or {}  # Ensure props is a dictionary, even if not provided
        self.parent = parent  # Add parent attribute

        # Set parent for each child
        for child in self.children:
            if child.parent is None:  # Avoid overwriting existing parent
                child.parent = self  # Assign this node as the parent

    def to_html(self):
        # Debugging aid (optional, can be removed)
        print(f"DEBUG: Processing node (tag={self.tag}, value={self.value}, children={len(self.children)})")

        # Special case: skip empty <p> tags
        if self.tag == "p" and (self.value is None or not self.value.strip()):
            print(f"DEBUG: Skipping empty <p> tag (parent tag={self.parent.tag if self.parent else 'None'})")
            return ""

        if not self.children and self.value is None:  # Leaf node
            return f"<{self.tag}{self.props_to_html()}></{self.tag}>"
        # Case for nodes with children
        if self.children:
            children_html = "".join([child.to_html() for child in self.children])
            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

        # Special case: self-closing <img> tags
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"

        # Case for leaf nodes with values
        if self.value is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        # Handle empty nodes without value or children
        return f"<{self.tag}{self.props_to_html()}></{self.tag}>"

    def props_to_html(self):
        """Helper method to generate HTML string for properties."""
        if not self.props:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])


# Example of debugging it:
# root = HTMLNode("div", None, [
#     HTMLNode("p", "This is a paragraph"),
#     HTMLNode("img", None, [], {"src": "image.jpg"}),


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Add extra validation
        if value is None:
            print(f"Warning: LeafNode created with None value, tag={tag}")
            value = ""
        super().__init__(tag, value, None, props or {})
    
    def to_html(self):
        # Special case for img tags, which are self-closing
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        
        # For other tags with empty values
        if (self.value is None or self.value == "") and self.tag is not None:
            raise ValueError(f"All leaf nodes must have a value (tag={self.tag})")
        
        # Normal case
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    




class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # We don't pass value to the parent constructor
        super().__init__(tag, None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have children.")        
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    


