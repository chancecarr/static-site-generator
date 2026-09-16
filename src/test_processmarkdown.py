import unittest
from processmarkdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_html_node
)
from textnode import TextType, TextNode

class TestProcessMarkdown(unittest.TestCase):
    def test_split_delimiter_basic(self):
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

    def test_split_delimiter_multiple(self):
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

    def test_split_delimiter_bold(self):
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

    def test_split_delimiter_italic(self):
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

    def test_split_delimiter_no_closer(self):
        node = TextNode("This is text with a **mistake in it", TextType.TEXT)
        self.assertRaisesRegex(Exception, "missing closing delimiter", split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_split_delimiter_not_text(self):
        node = TextNode("This is _text_ typed as TextType.BOLD", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is _text_ typed as TextType.BOLD", TextType.BOLD),
            ]
        )

    def test_split_delimiter_no_change(self):
        node = TextNode("This is text with no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with no delimiter", TextType.TEXT),
            ]
        )

    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with two images: ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with two links: [link1](https://www.google.com) and [link2](https://www.google.com)"
        )
        self.assertListEqual([("link1", "https://www.google.com"), ("link2", "https://www.google.com")], matches)

    def test_extract_links_mistake(self):
        matches = extract_markdown_links(
            "This is text with no valid [link](https://www.google.com"
        )
        self.assertListEqual([], matches)

    def test_extract_images_mistake(self):
        matches = extract_markdown_images(
            "This is text with no valid [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_links_ignore_image(self):
            matches = extract_markdown_links(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) but no link"
            )
            self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_image_no_change(self):
        node = TextNode("This is text with no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no image", TextType.TEXT),
            ]
        )

    def test_split_link_no_change(self):
        node = TextNode("This is text with no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no link", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
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
        )

    def test_text_to_textnodes_no_nested(self):
        text = "This is **text _with_** a nested italic"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text _with_", TextType.BOLD),
                TextNode(" a nested italic", TextType.TEXT)
            ]
        )

    def test_markdown_to_blocks_basic(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = "\n\n\n\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
###### This is an h6

### This is an h3

# This is an h1 with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is an h6</h6><h3>This is an h3</h3><h1>This is an h1 with <b>bold</b> text</h1></div>",
        )