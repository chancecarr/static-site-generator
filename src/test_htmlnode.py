import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Dummy text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode("a", "Link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode("body", None, [HTMLNode("p", "Dummy text"), HTMLNode("a", "Link", None, {"href": "https://www.google.com", "target": "_blank"})])
        self.assertEqual(str(node), "HTMLNode(body, None, [HTMLNode(p, Dummy text, None, None), HTMLNode(a, Link, None, {'href': 'https://www.google.com', 'target': '_blank'})], None)")