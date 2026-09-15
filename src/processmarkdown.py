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

def extract_markdown_images(text) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
