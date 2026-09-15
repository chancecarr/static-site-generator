import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
            parent_node = ParentNode("div", [])
            self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_multiple_children(self):
        child_1_node = LeafNode("b", "child 1")
        child_2_node = LeafNode("b", "child 2")
        parent_node = ParentNode("div", [child_1_node, child_2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child 1</b><b>child 2</b></div>",
        )