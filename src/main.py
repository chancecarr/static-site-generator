from generatecontent import copy_from_source_to_destination, generate_pages_recursive
import sys

def main():
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    copy_from_source_to_destination("./static", "./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

if __name__ == "__main__":
    main()