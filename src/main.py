from generatecontent import copy_from_source_to_destination, generate_page

def main():
    copy_from_source_to_destination("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
    main()