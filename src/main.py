"""Entry module for python code"""

from textfunctions import *
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from staticfunctions import copy_from_static_to_public, generate_page, generate_pages_recursive

def main()->'str':
    """Entry function for python code"""
    copy_from_static_to_public(
        "/Users/jrpatton/Documents/Code/BootDev/staticsite/static",
        "/Users/jrpatton/Documents/Code/BootDev/staticsite/public"
    )

    generate_pages_recursive(
        "/Users/jrpatton/Documents/Code/BootDev/staticsite/content",
        "/Users/jrpatton/Documents/Code/BootDev/staticsite/template.html",
        "/Users/jrpatton/Documents/Code/BootDev/staticsite/public"
    )

main()
