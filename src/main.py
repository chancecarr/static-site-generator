from textnode import TextNode, Text

def main():
    text_node = TextNode("Dummy text", Text.LINK, "https://www.boot.dev")
    print(text_node)

if __name__ == "__main__":
    main()