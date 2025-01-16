import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_basic(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual('<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>', node.to_html())

    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children(self):
        node = ParentNode(
            "p",
            [],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_props_on_parent(self):
        dummy_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
            dummy_props
        )
        self.assertEqual('<p href="https://www.google.com" target="_blank"><b>Bold text</b></p>', node.to_html())

    def test_parent_with_child_parent(self):
        dummy_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = ParentNode(
            "p",
            [
                ParentNode(
                    "a", 
                    [
                        LeafNode("b", "Bold text"),
                    ],
                    dummy_props
                    ),
                LeafNode(None, "Normal text")
            ],
            dummy_props
        )
        self.assertEqual(
            '<p href="https://www.google.com" target="_blank"><a href="https://www.google.com" target="_blank"><b>Bold text</b></a>Normal text</p>',
            node.to_html()
        )