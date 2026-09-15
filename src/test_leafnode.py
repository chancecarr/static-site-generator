import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_basic(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_props(self):
            node = LeafNode("a", "Link", {"href": "https://www.google.com", "target": "_blank"})
            self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Link</a>')

    def test_repr(self):
        node = LeafNode("a", "Link", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(str(node), "LeafNode(a, Link, {'href': 'https://www.google.com', 'target': '_blank'})")