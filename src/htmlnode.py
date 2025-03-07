
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    def to_html(self): 
        raise NotImplementedError("to_html not implemented")
    def props_to_html(self):
        if not self.props:
            return ""
        props = []
        for key, value in self.props.items():
            props.append(f'{key}="{value}"')
        return " " + " ".join(props)
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # We don't pass children to the parent constructor
        # and we ensure value is required
        super().__init__(tag, value, None, props=props)
    
    def to_html(self):
        if self.value is None or self.value == "":
            raise ValueError("All leaf nodes must have a value")
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
    


