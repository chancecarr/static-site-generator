import unittest
from processmarkdown import split_nodes_delimiter
from textnode import TextType, TextNode

class TestProcessMarkdown(unittest.TestCase):
    def test_split_nodes_basic(self):
        node = TextNode("This is text with a `code block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" in it", TextType.TEXT)
            ]
        )

    def test_split_nodes_multiple(self):
        node = TextNode("This is text with two `code` `blocks` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with two ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("blocks", TextType.CODE),
                TextNode(" in it", TextType.TEXT)
            ]
        )

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold** word in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word in it", TextType.TEXT)
            ]
        )

    def test_split_nodes_italic(self):
        node = TextNode("This is text with an _italic_ word in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word in it", TextType.TEXT)
            ]
        )

    def test_split_nodes_no_closer(self):
        node = TextNode("This is text with a **mistake in it", TextType.TEXT)
        self.assertRaisesRegex(Exception, "missing closing delimiter", split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_split_nodes_not_text(self):
        node = TextNode("This is _text_ typed as TextType.BOLD", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is _text_ typed as TextType.BOLD", TextType.BOLD),
            ]
        )

    def test_split_nodes_no_change(self):
            node = TextNode("This is text with no delimiter", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
            self.assertEqual(
                new_nodes,
                [
                    TextNode("This is text with no delimiter", TextType.TEXT),
                ]
            )
        