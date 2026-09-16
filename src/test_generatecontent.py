import unittest
from generatecontent import extract_title

class TestGenerateContent(unittest.TestCase):
    def test_extract_title_basic(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_extract_title_no_title(self):
        md = "This markdown has no title"
        self.assertRaisesRegex(Exception, "no title found", extract_title, md)

    def test_extract_title_buried_title(self):
        md = """
### Not the title
## Still not the title
# This is the title
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

    def test_extract_title_multiple_titles(self):
        md = """
# We only care about the first title
# Not this one
"""
        title = extract_title(md)
        self.assertEqual(title, "We only care about the first title")