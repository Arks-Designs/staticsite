"""Module for leaf of html (no children)"""

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """Class representing an html node with no children"""
    def __init__(self,
                 tag: str|None,
                 value: str,
                 children: None = None,
                 props: dict[str,str]|None = None):
        children = None
        super().__init__(tag, value, children, props)

    def to_html(self)->str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
