import unittest
from split_blocks import markdown_to_blocks
from split_blocks import block_to_block_type
from split_blocks import BlockType
from split_blocks import extract_title
from split_blocks import markdown_to_html_node
import unittest

class TestBlockToBlockType(unittest.TestCase):
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.code)
        self.assertEqual(block_to_block_type("```\n```"), BlockType.code)
        self.assertNotEqual(block_to_block_type("Regular text"), BlockType.code)
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), BlockType.ordered_list)
        self.assertEqual(block_to_block_type("10. Tenth item"), BlockType.ordered_list)
        self.assertNotEqual(block_to_block_type("1.ItemWithoutSpace"), BlockType.ordered_list)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a paragraph"), BlockType.paragraph)
        self.assertNotEqual(block_to_block_type("# Heading"), BlockType.paragraph)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("   \n\n   "), [])    

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("Just one block"), ["Just one block"])

    def test_multiple_blank_lines(self):
        self.assertEqual(
            markdown_to_blocks("Block 1\n\n\n\nBlock 2"),
            ["Block 1", "Block 2"]
        )   

    def test_leading_trailing_blank_lines(self):
        self.assertEqual(
            markdown_to_blocks("\n\nBlock 1\n\nBlock 2\n\n"),
            ["Block 1", "Block 2"]
        )



class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_paragraph_block():
        md = "This is a simple paragraph with no formatting."
        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == "<div><p>This is a simple paragraph with no formatting.</p></div>"
        
    def test_heading_block():
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == "<div><h1>This is a heading</h1></div>"     

    def test_code_block():
        md = "```\ndef code_block():\n    pass\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == "<div><pre><code>def code_block():\n    pass\n</code></pre></div>"

    def test_unordered_list():
        md = "* Item 1\n* Item 2\n* Item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"

    def test_ordered_list():
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"



import unittest

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_title_with_extra_whitespace(self):
        markdown = "#     Lots of spaces    "
        self.assertEqual(extract_title(markdown), "Lots of spaces")
    
    def test_title_not_on_first_line(self):
        markdown = "\n\n# Title on third line"
        self.assertEqual(extract_title(markdown), "Title on third line")
    
    def test_no_title(self):
        markdown = "This markdown has no title"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_only_second_level_headers(self):
        markdown = "## This is h2, not h1"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()





if __name__ == "__main__":
    unittest.main()