import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_children(self):
        node1 = LeafNode("a", "test value", [LeafNode(None, None,)], None)
        self.assertIsNone(node1.children)

    def test_to_html_with_props(self):
        dummy_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = LeafNode(
            "testtag",
            "testvalue",
            None,
            dummy_props
        )
        self.assertEqual(node1.to_html(), '<testtag href="https://www.google.com" target="_blank">testvalue</testtag>')

    def test_to_html_without_props(self):
        node1 = LeafNode(
            "testtag",
            "testvalue",
            None,
            None
        )
        self.assertEqual(node1.to_html(), '<testtag>testvalue</testtag>')

    def test_no_value_error(self):
        dummy_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = LeafNode(
            "testtag",
            None,
            None,
            dummy_props
        )
        with self.assertRaises(ValueError):
            node1.to_html()

    def test_no_tag_error(self):
        dummy_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = LeafNode(
            None,
            "testvalue",
            None,
            dummy_props
        )
        self.assertEqual("testvalue", node1.to_html())
