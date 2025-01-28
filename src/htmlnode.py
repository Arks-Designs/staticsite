"""Module to create HTML node representing an HTML block and content"""
from typing import Self

class HTMLNode():
    """Class representing HTML Block"""
    def __init__(
            self,
            tag: str | None = None,
            value: str | None = None,
            children: list[Self] | None = None,
            props: dict[str, str] | None = None
        ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Replaced by children, converts to HTMLS"""
        raise NotImplementedError()

    def props_to_html(self)->str:
        """Converts props into an html string"""
        # href="https://www.google.com" target="_blank"
        if self.props is None:
            return ""
        return "".join([f' {key}="{val}"' for key,val in self.props.items()])

    def __repr__(self)->str:
        res = f"HTMLNode({self.tag}, {self.value})\n"
        if self.children:
            res += f"Children: {self.children}\n"

        if self.props:
            res += "Props Keys           Values\n-----------------------\n"
            for key, val in self.props.items():
                res += f"{key}                  {val}\n"
        return res

    def __eq__(self, other_node):
        return (self.tag, self.value, self.children, self.props) == \
            (other_node.tag, other_node.value, other_node.children, other_node.props)
