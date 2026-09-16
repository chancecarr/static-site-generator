from os import path, listdir, mkdir, makedirs
from shutil import copy, rmtree
import re
from processmarkdown import markdown_to_html_node

def copy_from_source_to_destination(source_dir: str, destination_dir: str) -> None:
    abs_source = path.abspath(source_dir)
    abs_dest = path.abspath(destination_dir)
    print(f"copying directory {source_dir} to {destination_dir}")
    if not path.exists(abs_source): raise ValueError("invalid source directory")
    if not path.exists(abs_dest): raise ValueError("invalid destination directory")

    rmtree(destination_dir)
    mkdir(destination_dir)

    source_children = listdir(source_dir)
    for child in source_children:
        src_child = path.join(source_dir, child)
        dest_child = path.join(destination_dir, child)
        if path.isfile(src_child):
            print(f"copying file {src_child} to {dest_child}")
            copy(src_child, dest_child)
        else:
            mkdir(dest_child)
            copy_from_source_to_destination(src_child, dest_child)


def extract_title(markdown: str) -> str:
    matches: list[str] = re.findall(r"^# .*(?:\n|$)", markdown, re.M)
    if not matches:
        raise Exception("no title found")
    return matches[0].strip().removeprefix("# ")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file, open(template_path, "r") as template_file:
        md = from_file.read()
        title = extract_title(md)
        inner_content = markdown_to_html_node(md).to_html()
        outer_content = template_file.read()
        titled_content = outer_content.replace("{{ Title }}", title)
        final_content = titled_content.replace("{{ Content }}", inner_content)

        makedirs(path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as dest_file:
            dest_file.write(final_content)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for child in listdir(dir_path_content):
        src_child_path = path.join(dir_path_content, child)
        dest_child_path = path.join(dest_dir_path, child)
        if path.isfile(src_child_path):
            generate_page(src_child_path, template_path, dest_child_path.replace(".md", ".html"))
        else:
            mkdir(dest_child_path)
            generate_pages_recursive(src_child_path, template_path, dest_child_path)
    
