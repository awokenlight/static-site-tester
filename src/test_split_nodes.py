import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter  # Adjust this import path!
from split_nodes import split_nodes_image  # Adjust this import path!
from split_nodes import split_nodes_link  # Adjust this import path!
from split_nodes import text_to_textnodes  # Adjust this import path!



class SplitNodesTests(unittest.TestCase):
    def test_basic_delimiter(self):
        node = TextNode("This is `code` text.", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_no_delimiter(self):
        node = TextNode("This has no delimiter.", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This has no delimiter.", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_unbalanced_delimiter(self):
        node = TextNode("This `code has no end.", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Unbalanced delimiter: `")
        
def test_with_a_single_image(self):
    node = TextNode(
        "This is text with an image ![example](https://example.com/image.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    
    self.assertListEqual(new_nodes, [
        TextNode("This is text with an image ", TextType.TEXT),
        TextNode("example", TextType.IMAGE, "https://example.com/image.png"),
    ])

def test_with_multiple_images(self):
    node = TextNode(
        "Here is one ![image1](https://example.com/1.png) and another ![image2](https://example.com/2.png)",
        TextType.TEXT
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(new_nodes, [
        TextNode("Here is one ", TextType.TEXT),
        TextNode("image1", TextType.IMAGE, "https://example.com/1.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("image2", TextType.IMAGE, "https://example.com/2.png"),
    ])

def test_with_leading_image(self):
    node = TextNode(
        "![first](https://example.com/first.png)![second](https://example.com/second.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(new_nodes, [
        TextNode("first", TextType.IMAGE, "https://example.com/first.png"),
        TextNode("second", TextType.IMAGE, "https://example.com/second.png"),
    ])
    
def test_with_single_link(self):
    node = TextNode(
        "Check out [Boot.dev](https://www.boot.dev) for more!",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(new_nodes, [
        TextNode("Check out ", TextType.TEXT),
        TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" for more!", TextType.TEXT),
    ])
    

def test_with_multiple_links(self):
    node = TextNode(
        "Here is [Google](https://google.com) and [YouTube](https://youtube.com).",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(new_nodes, [
        TextNode("Here is ", TextType.TEXT),
        TextNode("Google", TextType.LINK, "https://google.com"),
        TextNode(" and ", TextType.TEXT),
        TextNode("YouTube", TextType.LINK, "https://youtube.com"),
        TextNode(".", TextType.TEXT),
    ])


def test_with_no_links(self):
    node = TextNode("This has no links.", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual(new_nodes, [TextNode("This has no links.", TextType.TEXT)])
    


def test_text_to_textnodes():
    # Test with a simple example
    text = "This is **text** with an _italic_ word and a `code block`"
    nodes = text_to_textnodes(text)
    
    # Assert the correct number of nodes
    assert len(nodes) == 6
    
    # Check a few specific nodes
    assert nodes[0].text == "This is "
    assert nodes[0].text_type == TextType.TEXT
    
    assert nodes[1].text == "text"
    assert nodes[1].text_type == TextType.BOLD
    
    # Add more assertions as needed
    assert nodes[2].text == " with an "
    assert nodes[2].text_type == TextType.TEXT
    
    assert nodes[3].text == "italic"
    assert nodes[3].text_type == TextType.ITALIC
    
    assert nodes[4].text == " word and a "
    assert nodes[4].text_type == TextType.TEXT
    
    assert nodes[5].text == "code block"
    assert nodes[5].text_type == TextType.CODE
def test_text_to_textnodes_with_links_and_images():
    text = "This is a [link](https://boot.dev) and an ![image](https://example.com/img.png)"
    nodes = text_to_textnodes(text)
    
    assert len(nodes) == 5
    
    # Test link node
    assert nodes[1].text == "link"
    assert nodes[1].text_type == TextType.LINK
    assert nodes[1].url == "https://boot.dev"
    
    # Test image node
    assert nodes[3].text == "image"
    assert nodes[3].text_type == TextType.IMAGE
    assert nodes[3].url == "https://example.com/img.png"