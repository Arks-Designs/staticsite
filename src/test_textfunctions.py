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

    def test_markdown_to_block(self):
        text = """# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        expected_results = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item""",
        ]
        self.assertEqual(markdown_to_blocks(text), expected_results)

    def test_markdown_to_block_single_line(self):
        text = """# This is a heading"""
        expected_results = [
            "# This is a heading",
        ]
        self.assertEqual(markdown_to_blocks(text), expected_results)

    def test_markdown_to_block_trailing_spaces(self):
        text = """# This is a heading                    

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        expected_results = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item""",
        ]
        self.assertEqual(markdown_to_blocks(text), expected_results)

    def test_block_to_block_type_heading_1(self):
        block = "# test block"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_block_to_block_type_heading_2(self):
        block = "###### test block"
        self.assertEqual(block_to_block_type(block), "heading")
    
    def test_block_to_block_type_heading_too_many_hash(self):
        block = "####### test block"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_heading_header_but_paragraph(self):
        block = "test start ##### test block"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_heading_multiline(self):
        block = """### heading
            should still work"""
        self.assertEqual(block_to_block_type(block), "heading")

    def test_block_to_block_type_code(self):
        block = "```code block test```"
        self.assertEqual(block_to_block_type(block), "code")
    
    def test_block_to_block_type_code_not_enough_ticks(self):
        block = "``code block test``"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_code_not_enough_ticks(self):
        block = "``code block test``"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_code_big_block(self):
        block = """```code block 
        test```"""
        self.assertEqual(block_to_block_type(block), "code")

    def test_block_to_block_type_quote(self):
        block = """>test test
> test test test"""
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_empty(self):
        block = """"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_unordered_dash(self):
        block = """- asdfasdf
- asdfasdf
- asfasdf"""
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_unordered_star(self):
        block = """* asdfasdf
* asdfasdf
* asfasdf"""
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_unordered_mixed(self):
        block = """- asdfasdf
* asdfasdf
- asfasdf"""
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_unordered_missing_space(self):
        block = """-asdfasdf
- asdfasdf
- asfasdf"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_ordered(self):
        block = """1. asdfasdf
2. asdfasdf
3. asfasdf"""
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_block_type_ordered_missing_space(self):
        block = """1.asdfasdf
2. asdfasdf
3. asfasdf"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_ordered_wrong_order(self):
        block = """1. asdfasdf
3. asdfasdf
2. asfasdf"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_markdown_to_html(self):
        text = """1. hello *there*
2. ![abc](hello.com)"""
        expected_results = HTMLNode("div", None, [
            HTMLNode("ol", None, [
                HTMLNode("li", None, [
                    HTMLNode(None, "hello "),
                    HTMLNode("i", "there")
                ]),
                HTMLNode("li", None, [
                    HTMLNode("img", None, None, {'src': 'hello.com', 'alt': 'abc'})
                ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(text), expected_results)

    def test_markdown_to_html_multi_blocks(self):
        text = """```What can we do in a code block```

### This is a tier 3 header

* line 1
* line 2 *italics*

Random set of text [abc](test.com)
Random set of **text 2**

>Quote line 1
>Quote line 2"""
        expected_results = HTMLNode("div", None, [
            HTMLNode("pre", None, [
                HTMLNode("code", None, [
                    HTMLNode(None, "What can we do in a code block")
                ])
            ]),
            HTMLNode("h3", None, [
                HTMLNode(None, "This is a tier 3 header")
            ]),
            HTMLNode("ul", None, [
                HTMLNode("li", None, [
                    HTMLNode(None, "line 1")
                ]),
                HTMLNode("li", None, [
                    HTMLNode(None, "line 2 "),
                    HTMLNode("i", "italics")
                ])
            ]),
            HTMLNode("p", None, [
                HTMLNode(None, "Random set of text "),
                HTMLNode("a", "abc", None, {"href": "test.com"}),
                HTMLNode(None, "\nRandom set of "),
                HTMLNode("b", "text 2")
            ]),
            HTMLNode("blockquote", None, [
                HTMLNode(None, "Quote line 1\nQuote line 2")
            ])
        ])
        self.assertEqual(markdown_to_html_node(text), expected_results)

    def test_extract_title(self):
        text = """# Sample heading

### Sample heading two

* list one
* list two

some random text"""
        self.assertEqual(extract_title(text), "Sample heading")

    def test_extract_title_not_first(self):
        text = """### Sample heading two

# Sample heading

* list one
* list two

some random text"""
        self.assertEqual(extract_title(text), "Sample heading")

    def test_extract_title_random_white_space(self):
        text = """### Sample heading two

#     Sample heading      

* list one
* list two

some random text"""
        self.assertEqual(extract_title(text), "Sample heading")

    def test_extract_title_multiple_headings(self):
        text = """# Sample heading

# Sample heading two

* list one
* list two

some random text"""
        self.assertEqual(extract_title(text), "Sample heading")

    def test_extract_title_no_heading(self):
        text = """* list one
* list two

some random text"""
        with self.assertRaises(ValueError):
            extract_title(text)


if __name__ == "__main__":
    unittest.main()
