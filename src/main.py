"""Entry module for python code"""

from textfunctions import *
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from staticfunctions import copy_from_static_to_public

def main()->'str':
    """Entry function for python code"""
    dummy_text_node = TextNode(
        "This is some sample text",
        TextType.LINK,
        "https://sample-url.com"
    )

    #print(dummy_text_node)

    dummy_props = {
    "href": "https://www.google.com",
    "target": "_blank",
}

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    copy_from_static_to_public("static", "public")


main()
