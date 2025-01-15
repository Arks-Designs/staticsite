"""Entry module for python code"""

from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main()->'str':
    """Entry function for python code"""
    dummy_text_node = TextNode(
        "This is some sample text",
        TextType.LINK,
        "https://sample-url.com"
    )

    print(dummy_text_node)

    dummy_props = {
    "href": "https://www.google.com",
    "target": "_blank",
}

    dummy_html_node = HTMLNode(
        "testtag",
        "testvalue",
        None,
        dummy_props
    )

    print(dummy_html_node.props_to_html())
    print(repr(dummy_html_node))

main()
