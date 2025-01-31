"""Module to work with markdown text"""

import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

def split_nodes_delimiter(nodes: list[TextNode], delimiter: str, text_type: TextType)->list[TextNode]:
    """Module to split a line of markdown into text nodes"""
    results = []
    for node in nodes:
        split_text = node.text.split(delimiter)
        if len(split_text) == 1:
            results.append(node)
        else:
            if node.text.startswith(delimiter) and node.text.endswith(delimiter):
                results.append(TextNode(split_text[1], text_type))
            elif node.text.startswith(delimiter):
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

def block_to_block_type(block:str)->str:
    """Module to determine the type of a block
    options are paragraph, heading, code, quote,
    unordered_list, ordered_list"""
    if re.match(r"#{1,6} .+", block):
        return "heading"
    
    if block[:3] == "```" and block[-3:] == "```":
        return "code"
    
    split_lines = block.split("\n")
    num_lines = len(split_lines)
    if len(list(filter(lambda x: x.startswith(">"), split_lines))) == num_lines:
        return "quote"
    
    unordered_cond = lambda x: x[:2] in ("* ", "- ")
    if len(list(filter(unordered_cond, split_lines))) == num_lines:
        return "unordered_list"
    
    count = 1
    ordered_list_flag = True
    for line in split_lines:
        if not line.startswith(f"{count}. "):
            ordered_list_flag = False
        count += 1
    if ordered_list_flag:
        return "ordered_list"

    return "paragraph"

def markdown_to_html_node(text:str)->HTMLNode:
    """Module to convert a markdown text to html"""
    blocks = markdown_to_blocks(text)
    block_html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        top_html_nodes = text_to_children(block, block_type)

        block_html_nodes.append(top_html_nodes)
    return ParentNode("div", block_html_nodes)

def strip_text_on_type(text:str, block_type:str)->str:
    """Module to strip text based on block type"""
    if block_type == "heading":
        heading_chars = r"#{1,6} "
        start = re.match(heading_chars, text).span()[1]
        return text[start:]
    
    if block_type == "code":
        return text[3:-3]
    
    split_lines = text.split("\n")
    if block_type == "quote":
        lines = list(map(lambda x: x[2:], split_lines))
        return "\n".join(lines)

    if block_type == "unordered_list":
        lines = list(map(lambda x: x[2:], split_lines))
        return "\n".join(lines)
    
    if block_type == "ordered_list":
        lines = list(map(lambda x: x[3:], split_lines))
        return "\n".join(lines)

    return text

def text_to_children(text:str, block_type:str)->list[HTMLNode]:
    """Module to take text and convert to html nodes"""

    cleaned_block = strip_text_on_type(text, block_type)

    if block_type in ["unordered_list", "ordered_list"]:
        lines = cleaned_block.split("\n")
        text_nodes = list(map(text_to_textnodes, lines))
        html_nodes = list(map(lambda y: list(map(lambda x: x.text_node_to_html_node(), y)), text_nodes))
        list_html_nodes = list(map(lambda x: ParentNode("li", x), html_nodes))

        if block_type == "unordered_list":
            return ParentNode("ul", list_html_nodes)

        if block_type == "ordered_list":
            return ParentNode("ol", list_html_nodes)

    text_nodes = text_to_textnodes(cleaned_block)
    html_nodes = list(map(lambda x: x.text_node_to_html_node(), text_nodes))

    if block_type == "quote":
        return ParentNode("blockquote", html_nodes)

    if block_type == "code":
        return ParentNode("pre", [ParentNode("code", html_nodes)])

    if block_type == "heading":
        heading_chars = r"#{1,6} "
        start = re.match(heading_chars, text).span()[1]
        heading_tag = f"h{start - 1}"
        return ParentNode(heading_tag, html_nodes)

    return ParentNode("p", html_nodes)

def extract_title(markdown):
    """Function to return the H1 heading line"""
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading":
            if block.startswith("# "):
                updated_text = block.replace("#", "", 1)
                updated_text = updated_text.strip()
                return updated_text
            
    raise ValueError("No h1 header in document")
