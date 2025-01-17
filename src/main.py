"""Entry module for python code"""

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

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

    node_t = TextNode(
            "This is some sample text",
            TextType.LINK,
            "https://sample-url.com"
        )
    node_l = LeafNode("a", "This is some sample text", None, {"href": "https://sample-url.com"})

    print(node_t.text_node_to_html_node())
    print("\n\n\n\n")
    print(node_l)
    print(node_t.text_node_to_html_node() == node_l)


main()
