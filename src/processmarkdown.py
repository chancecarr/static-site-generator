from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from blocktype import BlockType, block_to_block_type
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    collected_new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: 
            collected_new_nodes.append(old_node)
            continue
        current_new_nodes = []
            
        node_pieces = old_node.text.split(delimiter)

        if len(node_pieces) % 2 == 0:
            raise Exception("missing closing delimiter")
        
        for i in range(len(node_pieces)):
            if i % 2 == 0:
                current_new_nodes.append(TextNode(node_pieces[i], old_node.text_type, old_node.url))
            else:
                current_new_nodes.append(TextNode(node_pieces[i], text_type, old_node.url))
        collected_new_nodes.extend(current_new_nodes)

    return collected_new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    collected_new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        current_new_nodes = []
        text = old_node.text
        images = extract_markdown_images(text)

        if not images:
            collected_new_nodes.append(old_node)
            continue

        for alt, src in images:
            sections = text.split(f"![{alt}]({src})", 1)
            if sections[0] != "":
                current_new_nodes.append(TextNode(sections[0], TextType.TEXT))
            current_new_nodes.append(TextNode(alt, TextType.IMAGE, src))
            text = sections[1]

        if text != "":
            current_new_nodes.append(TextNode(text, TextType.TEXT))

        collected_new_nodes.extend(current_new_nodes)

    return collected_new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    collected_new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        current_new_nodes = []
        text = old_node.text
        links = extract_markdown_links(text)

        if not links:
            collected_new_nodes.append(old_node)
            continue

        for content, src in links:
            sections = text.split(f"[{content}]({src})", 1)
            if sections[0] != "":
                current_new_nodes.append(TextNode(sections[0], TextType.TEXT))
            current_new_nodes.append(TextNode(content, TextType.LINK, src))
            text = sections[1]

        if text != "":
            current_new_nodes.append(TextNode(text, TextType.TEXT))

        collected_new_nodes.extend(current_new_nodes)
        
    return collected_new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    original_node = TextNode(text, TextType.TEXT)
    nodes_split_by_bold = split_nodes_delimiter([original_node], "**", TextType.BOLD)
    nodes_split_by_italic = split_nodes_delimiter(nodes_split_by_bold, "_", TextType.ITALIC)
    nodes_split_by_code = split_nodes_delimiter(nodes_split_by_italic, "`", TextType.CODE)
    nodes_split_by_image = split_nodes_image(nodes_split_by_code)
    nodes_split_by_link = split_nodes_link(nodes_split_by_image)
    return nodes_split_by_link

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    return list(filter(lambda x: x != "", blocks))

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))

def heading_block_to_html_node(block: str) -> HTMLNode:
    heading = re.findall(r"^(#+) ", block)[0]
    if not heading: raise Exception("no heading found")

    text = re.findall(r"^#+ (.*)(?:\n|$)", block)[0]
    if not text: raise Exception("no text found")

    tag = f"h{len(heading)}"
    return ParentNode(tag, text_to_children(text))

def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = re.findall(r"^- (.*)(?:\n|$)", block, re.M)
    children = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", children)   

def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = re.findall(r"^\d+\. (.*)(?:\n|$)", block, re.M)
    children = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", children)

def blockquote_to_html_node(block: str) -> HTMLNode:
    items = re.findall(r"^> *(.*)(?:\n|$)", block, re.M)
    return ParentNode("blockquote", text_to_children(" ".join(items)))

def code_to_html_node(block: str) -> HTMLNode:
    items = re.findall(r"```\n(.*)```", block, re.DOTALL)
    if not items: raise Exception("no code found")
    return ParentNode("pre", [LeafNode("code", items[0])])

def blocktype_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block.replace("\n", " ")))
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return blockquote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise Exception("unknown block type")

def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_nodes: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        node = blocktype_to_html_node(block, block_type)
        html_nodes.append(node)
    return ParentNode("div", html_nodes)

