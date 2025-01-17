"""Class for inline text in our doc"""
from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    """Enum representing the text type"""
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    """Class to capture inline text"""
    def __init__(self, text:str|None, text_type: TextType, url:str|None = None):
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

    def text_node_to_html_node(self):
        """Module to convert text to leafnode html"""
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text, None, None)
            case TextType.BOLD:
                return LeafNode("b", self.text, None, None)
            case TextType.ITALIC:
                return LeafNode("i", self.text, None, None)
            case TextType.CODE:
                return LeafNode("code", self.text, None, None)
            case TextType.LINK:
                return LeafNode("a", self.text, None, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode(
                    "img",
                    None,
                    None,
                    {"src": self.url, "alt":self.text}
                )
            case _:
                raise ValueError("Invalid text type")
