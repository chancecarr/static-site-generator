from textnode import TextNode, TextType
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
