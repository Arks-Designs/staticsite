"""Module to work with markdown text"""

import re
from textnode import TextNode, TextType

def split_nodes_delimiter(nodes: list[TextNode], delimiter: str, text_type: TextType)->list[TextNode]:
    """Module to split a line of markdown into text nodes"""
    results = []
    for node in nodes:
        split_text = node.text.split(delimiter)
        if len(split_text) == 1:
            results.append(node)
        else:
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

def split_nodes(nodes: list[TextNode], split_type:str)->list[TextNode]:
    """Module to split nodes with a line of markdown into text and images"""
    if split_type not in ["image", "link"]:
        raise ValueError("Split nodes type must be 'link' or 'image'")
    results = []
    for node in nodes:
        results += split_node(node, split_type)
    return results

def split_node(node:TextNode, split_type:str)->list[TextNode]:
    """Module to split a line of markdown into text and images"""
    if split_type not in ["image", "link"]:
        raise ValueError("Split nodes type must be 'link' or 'image'")
    results = []
    if len(node.text) == 0:
        return None

    if split_type == "image":
        objs = extract_markdown_images(node.text)
    else:
        objs = extract_markdown_links(node.text)

    #print(images)
    if len(objs) == 0:
        results.append(TextNode(node.text, node.text_type, node.url))
        return results

    if split_type == "image":
        first = f"![{objs[0][0]}]({objs[0][1]})"
        text_type = TextType.IMAGE
    else:
        first = f"[{objs[0][0]}]({objs[0][1]})"
        text_type = TextType.LINK

    first_index = node.text.find(first)
    if first_index != 0:
        results.append(TextNode(node.text[:first_index], node.text_type, node.url))
    results.append(TextNode(objs[0][0], text_type, objs[0][1]))


    new_node = TextNode(node.text[first_index + len(first):], node.text_type, node.url)
    recursion_results = split_node(new_node, split_type)
    if recursion_results is not None:
        results += recursion_results

    return results

def extract_markdown_images(text:str)->list[(str,str)]:
    """Module to return image text and url from input text"""
    results = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return results

def extract_markdown_links(text:str)->list[(str,str)]:
    """Module to return link text and url from input text"""
    results = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return results

def text_to_textnodes(text:str)->list[TextNode]:
    """Module to combine functions to convert text string to list of TextNodes"""
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes(nodes, "image")
    nodes = split_nodes(nodes, "link")
    return nodes

def markdown_to_blocks(markdown:str)->list[str]:
    """Module to break documents into blocks"""
    blocks = markdown.split("\n\n")
    blocks = list(map(str.strip, blocks))
    blocks = list(filter(lambda x: x not in ("", "\n"), blocks))
    return blocks
