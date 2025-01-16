"""Module to handle parent html elements (not leaf)"""

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    """Class representing nodes that are not leafs"""
    def __init__(self,
                 tag: str,
                 children: list[HTMLNode]|None = None,
                 props: dict[str,str]|None = None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self)->str:
        if self.tag is None:
            raise ValueError("Tag required on parent node")
        if self.children is None or self.children == []:
            raise ValueError("Parent node must have children")
        children_result = "".join([child.to_html() for child in self.children])
        result = f"<{self.tag}{self.props_to_html()}>{children_result}</{self.tag}>"
        return result
