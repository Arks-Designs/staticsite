"""Class for inline text in our doc"""
from enum import Enum

class TextType(Enum):
    """Enum representing the text type"""
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    """Class to capture inline text"""
    def __init__(self:'TextNode', text:'str', text_type:'TextType', url:'str'=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self:'TextNode', other_text_node:'TextNode')->'bool':
        """Compares properties of two text nodes"""
        cond_1 = self.text      == other_text_node.text
        cond_2 = self.text_type == other_text_node.text_type
        cond_3 = self.url       == other_text_node.url
        return cond_1 and cond_2 and cond_3

    def __repr__(self:'TextNode')->'str':
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
