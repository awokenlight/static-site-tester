from enum import Enum
from htmlnode import HTMLNode
from node_transformations import text_node_to_html_node
import re
from split_nodes import text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):

    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(block):
    block = block.strip()
    lines = block.split("\n")
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.code
    elif all(line.startswith(">") for line in lines):
        return BlockType.quote
    elif block.startswith("#") and " " in block:  # Ensure heading has a space after #
        return BlockType.heading
    elif all(line.strip().startswith(("- ", "* ", "+ ")) or not line.strip() for line in lines):
        # Allow empty lines in lists and recognize multiple list markers
        return BlockType.unordered_list
    elif all(re.match(r"^\s*\d+\.\s+.+$", line) or not line.strip() for line in lines):
        # Allow empty lines in ordered lists
        return BlockType.ordered_list
    else:
        return BlockType.paragraph


def markdown_to_blocks(markdown):
    potential_blocks = markdown.split('\n\n')
    
    blocks = []
    for block in potential_blocks:
        stripped_block = block.strip()
        if stripped_block:
            blocks.append(stripped_block)
            
    return blocks




def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    parent_node = HTMLNode("div", None, [], {})  # tag, value, children, props
    
    # Define helper function
    def text_to_children(text):
        text_nodes = text_to_textnodes(text)
        html_nodes = []
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            html_nodes.append(html_node)
        return html_nodes
    
    # Process each block
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.paragraph:
            children = text_to_children(block)
            new_node = HTMLNode("p", None, children, {})  # tag, value, children, props
            parent_node.children.append(new_node)
        
        elif block_type == BlockType.heading:
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            
            text = block[level:].strip()
            children = text_to_children(text)
            new_node = HTMLNode(f"h{level}", None, children, {})  # CORRECT
            parent_node.children.append(new_node)
        
        elif block_type == BlockType.code:
            lines = block.split('\n')
            code_content = '\n'.join(lines[1:-1])
            
            # For code blocks, we don't process inline markdown
            code_text_node = TextNode(code_content, TextType.TEXT)
            code_html_node = text_node_to_html_node(code_text_node)
            
            # Create pre and code nodes
            code_node = HTMLNode("code", None, [code_html_node], {})  # CORRECT
            pre_node = HTMLNode("pre", None, [code_node], {})  # CORRECT
            
            # Add pre node as child to parent
            parent_node.children.append(pre_node)
            
        elif block_type == BlockType.quote:
            # Remove the > prefix from each line
            lines = block.split('\n')
            quote_lines = []
            for line in lines:
                if line.startswith('>'):
                    quote_lines.append(line[1:].strip())
                else:
                    quote_lines.append(line.strip())
            
            quote_text = ' '.join(quote_lines)
            children = text_to_children(quote_text)
            quote_node = HTMLNode("blockquote", None, children, {})  # CORRECT
            parent_node.children.append(quote_node)
            
            
            
        elif block_type == BlockType.unordered_list:
            lines = block.split('\n')
            ul_node = HTMLNode("ul", None, [], {})
            
            for line in lines:
                line = line.strip()
                if line.startswith(("- ", "* ", "+ ")):
                    item_text = line[2:]  # Remove the marker and space
                    
                    # Parse the text to maintain formatting
                    item_children = text_to_children(item_text)
                    
                    # Ensure the node is never a leaf without a value
                    if item_children:
                        li_node = HTMLNode("li", None, item_children, {})
                    else:
                        # If no formatted elements, use the text as the value
                        li_node = HTMLNode("li", item_text, [], {})
                    
                    ul_node.children.append(li_node)
            
            if ul_node.children:
                parent_node.children.append(ul_node)
            
            
        elif block_type == BlockType.ordered_list:
            lines = block.split('\n')
            ol_node = HTMLNode("ol", None, [], {})
            
            for line in lines:
                if line.strip() and line.strip()[0].isdigit():
                    # Find the first space after the number and period
                    for i, char in enumerate(line.strip()):
                        if char == ' ' and i > 0 and line.strip()[i-1] == '.':
                            item_text = line.strip()[i+1:]
                            break
                    else:
                        continue  # Skip if the line doesn't match the pattern
                    
                    item_children = text_to_children(item_text)
                    li_node = HTMLNode("li", None, item_children, {})
                    ol_node.children.append(li_node)
            
            parent_node.children.append(ol_node)
    
    return parent_node




def extract_title(markdown_content):
    
    lines = markdown_content.split("\n")
    for line in lines:
        print(f"DEBUG: Checking line for title: '{line}'")
        if line.strip().startswith("# "):  
            return line.strip()[2:]
    raise Exception("No title found")