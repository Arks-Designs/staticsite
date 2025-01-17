import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node 1", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://url.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://url_not.com")
        self.assertNotEqual(node, node2)

    def test_to_html_link(self):
        node = TextNode(
            "This is some sample text",
            TextType.LINK,
            "https://sample-url.com"
        )
        self.assertEqual(
            node.text_node_to_html_node(),
            LeafNode("a", "This is some sample text", None, {"href": "https://sample-url.com"})
            )
        
    def test_to_html_text(self):
        node = TextNode(
            "This is some sample text",
            TextType.TEXT,
        )
        self.assertEqual(
            node.text_node_to_html_node(),
            LeafNode(None, "This is some sample text", None, None)
            )
        
    def test_to_html_bold(self):
        node = TextNode(
            "This is some sample text",
            TextType.BOLD,
        )
        self.assertEqual(
            node.text_node_to_html_node(),
            LeafNode("b", "This is some sample text", None, None)
            )
        
    def test_to_html_image(self):
        node = TextNode(
            "This is some sample text",
            TextType.IMAGE,
            "https://sample-url.com"
        )
        self.assertEqual(
            node.text_node_to_html_node(),
            LeafNode("img", None, None, {
                "alt": "This is some sample text",
                "src": "https://sample-url.com"
            })
            )
        
    def test_to_html_invalid(self):
        node = TextNode(
            "This is some sample text",
            None,
            "https://sample-url.com"
        )
        with self.assertRaises(ValueError):
            node.text_node_to_html_node()

if __name__ == "__main__":
    unittest.main()
