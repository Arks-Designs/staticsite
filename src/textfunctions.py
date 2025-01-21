"""Module to work with markdown text"""

from textnode import TextNode, TextType

def split_nodes_delimiter(nodes: list[TextNode], delimiter: str, text_type: TextType)->list[TextNode]:
    """Module to split a line of markdown into text nodes"""
    results = []
    for node in nodes:
        split_text = node.text.split(delimiter)
        if len(split_text) == 1:
            return node
        if node.text.startswith(delimiter):
            results.append(TextNode(split_text[1], text_type))
            results.append(TextNode(split_text[2], node.text_type))
        elif node.text.endswith(delimiter):
            results.append(TextNode(split_text[0], node.text_type))
            results.append(TextNode(split_text[1], text_type))
        else:
            results.append(TextNode(split_text[0], node.text_type))
            results.append(TextNode(split_text[1], text_type))
            results.append(TextNode(split_text[2], node.text_type))
    return results
