from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{i}. ") for i, line in enumerate(block.split("\n"), start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH