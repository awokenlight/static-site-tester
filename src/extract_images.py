import re

def extract_markdown_images(text):
    images = []
    for match in re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text):
        images.append((match.group(1), match.group(2)))
    return images

def extract_markdown_links(text):
    links = []
    for match in re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text):
        links.append((match.group(1), match.group(2)))
    return links