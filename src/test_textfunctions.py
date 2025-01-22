import unittest 

from textnode import TextNode, TextType
from textfunctions import *

class TestTextFunctions(unittest.TestCase):
    def test_split_node_delim(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        exp_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), exp_result)

    def test_split_node_delim_multiple_nodes(self):
        node1 = TextNode("This is text with a **bold block** in it", TextType.TEXT)
        node2 = TextNode("This is **another block** of bold text", TextType.TEXT)
        exp_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("another block", TextType.BOLD),
            TextNode(" of bold text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node1, node2], "**", TextType.BOLD), exp_result)

    def test_split_node_delim_start(self):
        node = TextNode("*This is* text with a `code block` word", TextType.TEXT)
        exp_result = [
            TextNode("This is", TextType.ITALIC),
            TextNode(" text with a `code block` word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), exp_result)

    def test_split_node_delim_end(self):
        node = TextNode("This is text with a `code *block` word*", TextType.TEXT)
        exp_result = [
            TextNode("This is text with a `code ", TextType.TEXT),
            TextNode("block` word", TextType.ITALIC),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), exp_result)

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_results = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(extract_markdown_images(text), expected_results)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_results = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(extract_markdown_links(text), expected_results)

    def test_split_node_images(self):
        node = TextNode(
        "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev).",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "image")
        expected_results = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_image_no_image(self):
        node = TextNode(
        "This is text with a no links",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "image")
        expected_results = [
            TextNode("This is text with a no links", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_images_with_end_image(self):
        node = TextNode(
        "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "image")
        expected_results = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_images_with_start_image(self):
        node = TextNode(
        "![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev).",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "image")
        expected_results = [
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "link")
        expected_results = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_image_no_links(self):
        node = TextNode(
        "This is text with a no links",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "link")
        expected_results = [
            TextNode("This is text with a no links", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_images_with_end_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "link")
        expected_results = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_images_with_start_links(self):
        node = TextNode(
        "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], "link")
        expected_results = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_results)

    def test_split_node_invalid_type(self):
        node = TextNode(
        "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
        TextType.TEXT,
        )
        with self.assertRaises(ValueError):
            new_nodes = split_nodes([node], "invalid")

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_results = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected_results)


if __name__ == "__main__":
    unittest.main()
