import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Your existing test for equality
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertEqual(node.text, node2.text)
        self.assertNotEqual(node, None)
    
    def test_different_text_type(self):
        # Test what happens when text_type is different
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        
    def test_url_property(self):
        # Test behavior with url property
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")
        self.assertEqual(node, node2)   
        
        node3 = TextNode("Link text", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node3)
        
    def test_url_none(self):
        # Test behavior when url is None (the default)
        node = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.TEXT)
        self.assertEqual(node.url, None)
        self.assertEqual(node, node2)

    
if __name__ == "__main__":
    unittest.main()