from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"  # For text between backticks
    LINK = "link"  # This is the missing one
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text if text is not None else ""  # Convert None to empty string
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
    
    # Return string representation
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"