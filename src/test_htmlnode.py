import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode  # Adjust the import path as needed
from htmlnode import ParentNode  # Adjust the import path as needed
from node_transformations import text_node_to_html_node
from textnode import TextNode, TextType



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with empty props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        # Note: The order of properties in a dictionary isn't guaranteed
        # So we need to check if both attributes are present rather than the exact string
        html = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', html)
        self.assertIn(' target="_blank"', html)
        self.assertEqual(len(html.split()), 2)  # Should have 2 attributes
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me!")
        self.assertEqual(node.props, {"href": "https://www.google.com"})
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_no_value(self):
        node = LeafNode("div", "")
        with self.assertRaises(ValueError):
            node.to_html()






def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
def test_to_html_no_tag(self):
    node = ParentNode(None, [LeafNode("span", "text")])
    with self.assertRaises(ValueError):
        node.to_html()

def test_to_html_no_children(self):
    node = ParentNode("div", [])
    with self.assertRaises(ValueError):
        node.to_html()
def test_to_props_html_multiple_props(self):
    node = ParentNode("div", [LeafNode("span", "text")], props={"class": "container", "id": "main"})
    # The order of props might vary, so check for both possibilities
    prop_string = node.props_to_html()
    self.assertTrue(' class="container"' in prop_string and ' id="main"' in prop_string)

def test_to_html_with_multiple_children(self):
    child1 = LeafNode("span", "first")
    child2 = LeafNode("b", "second")
    child3 = LeafNode("i", "third")
    parent = ParentNode("div", [child1, child2, child3])
    self.assertEqual(parent.to_html(), "<div><span>first</span><b>second</b><i>third</i></div>")

def test_to_html_with_mixed_children(self):
    leaf1 = LeafNode("b", "bold")
    leaf2 = LeafNode("i", "italic")
    parent1 = ParentNode("p", [leaf1, leaf2])
    leaf3 = LeafNode("span", "text")
    parent2 = ParentNode("div", [parent1, leaf3])
    self.assertEqual(parent2.to_html(), "<div><p><b>bold</b><i>italic</i></p><span>text</span></div>")

def test_text_type_text(self):
        node = TextNode("This is plain text.", TextType.TEXT)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "This is plain text.")
        self.assertEqual(result.props, None)

def test_text_type_bold(self):
        node = TextNode("Bold text.", TextType.BOLD)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "Bold text.")
        self.assertEqual(result.props, None)

def test_text_type_image(self):
        node = TextNode("Alt text for image.", TextType.IMAGE, url="image_url.png")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, {"src": "image_url.png", "alt": "Alt text for image."})

def test_invalid_text_type_handling(self):
        node = TextNode("Invalid type.", "INVALID_TYPE")  # Simulating an unsupported case
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)














if __name__ == "__main__":
    unittest.main()
