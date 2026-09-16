from textnode import TextNode, TextType
from os import path, listdir, mkdir
from shutil import copy, rmtree

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


def main():
    copy_from_source_to_destination("./static", "./public")

if __name__ == "__main__":
    main()