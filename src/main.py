"""Entry module for python code"""

from textfunctions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    node = TextNode("This is text with a `code block`", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))



main()
