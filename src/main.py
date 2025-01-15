"""Entry module for python code"""

from textnode import TextNode, TextType

def main()->'str':
    """Entry function for python code"""
    dummy_text_node = TextNode(
        "This is some sample text",
        TextType.LINK,
        "https://sample-url.com"
    )

    print(dummy_text_node)

main()
