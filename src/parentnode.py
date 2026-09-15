from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None: raise ValueError("missing required tag")
        if self.children is None or self.children == []: raise ValueError("missing required children")
        children_html_list = [child.to_html() for child in self.children]
        children_html = "".join(children_html_list)
        if self.props is None or self.props == {}:
            return f"<{self.tag}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag} {super().props_to_html()}>{children_html}</{self.tag}>"
