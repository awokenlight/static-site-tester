from textnode import TextNode, TextType
from extract_images import extract_markdown_images
from extract_images import extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Helper function for splitting a single TextNode
    def split_text_node(node, delimiter, text_type):
        # Get the text from the node
        text = node.text
        
        # Find the first occurrence of the delimiter
        first_idx = text.find(delimiter)
        if first_idx == -1:
            # No delimiter? Return the original node in a list.
            return [node]
        
        # Find the matching closing delimiter (next occurrence)
        second_idx = text.find(delimiter, first_idx + len(delimiter))
        if second_idx == -1:
            # Raise an exception if no closing delimiter is found
            raise Exception(f"Unbalanced delimiter: {delimiter}")
        
        # Split the text into three parts: before, between, and after delimiters
        before = text[:first_idx]
        between = text[first_idx + len(delimiter):second_idx]
        after = text[second_idx + len(delimiter):]
        
        # Create new nodes based on the split
        new_nodes = []
        if before:
            new_nodes.append(TextNode(before, TextType.TEXT))  # Keep 'TEXT' type for 'before'
        new_nodes.append(TextNode(between, text_type))  # Assign the new type for 'between'
        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))  # Keep 'TEXT' type for 'after'

        return new_nodes

    # Main logic for processing all nodes
    new_nodes = []  # List to store processed nodes
    for old_node in old_nodes:
        # Only split 'TEXT' nodes
        if old_node.text_type == TextType.TEXT:
            new_nodes.extend(split_text_node(old_node, delimiter, text_type))
        else:
            # Keep other node types as-is
            new_nodes.append(old_node)  # Append the original node

    return new_nodes
   




def split_nodes_image(old_nodes):
    new_nodes = []  # This will hold the resulting split nodes

    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            # Extract all images in the current text node
            images = extract_markdown_images(old_node.text)
            
            if images:
                # Track where we are in the text as we split it
                start_idx = 0
                
                for alt, src in images:
                    # Construct the markdown for the image
                    image_markdown = f"![{alt}]({src})"
                    
                    # Find the position of the image markdown
                    split_idx = old_node.text.find(image_markdown, start_idx)
                    
                    # Extract and append text before the image
                    before_text = old_node.text[start_idx:split_idx]
                    if before_text:
                        new_nodes.append(TextNode(before_text, TextType.TEXT))
                    
                    # Add the image node
                    new_nodes.append(TextNode(alt, TextType.IMAGE, src))
                    
                    # Update start index to after this image markdown
                    start_idx = split_idx + len(image_markdown)
                
                # Handle any trailing text after the last image
                remaining_text = old_node.text[start_idx:]
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                # If no images, keep the node unchanged
                new_nodes.append(old_node)
        else:
            # Non-text types are appended as is
            new_nodes.append(old_node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []  # This will hold the resulting split nodes

    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            # Extract all links in the current text node
            links = extract_markdown_links(old_node.text)
            
            if links:
                # Track where we are in the text as we split it
                start_idx = 0
                
                for link_text, url in links:
                    # Construct the markdown for the link
                    link_markdown = f"[{link_text}]({url})"
                    
                    # Find the position of the link markdown
                    split_idx = old_node.text.find(link_markdown, start_idx)
                    
                    # Extract and append text before the link
                    before_text = old_node.text[start_idx:split_idx]
                    if before_text:
                        new_nodes.append(TextNode(before_text, TextType.TEXT))
                    
                    # Add the link node
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                    
                    # Update start index to after this link markdown
                    start_idx = split_idx + len(link_markdown)
                
                # Handle any trailing text after the last link
                remaining_text = old_node.text[start_idx:]
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                # If no links, keep the node unchanged
                new_nodes.append(old_node)
        else:
            # Non-text types are appended as is
            new_nodes.append(old_node)

    return new_nodes


def text_to_textnodes(text):
    # Initialize the list of text nodes
    text_nodes = [TextNode(text, TextType.TEXT)]
    
    # Split nodes for images and links
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    
    return text_nodes