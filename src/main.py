from textnode import TextNode, TextType
import os
import shutil
from htmlnode import HTMLNode
from split_blocks import markdown_to_html_node, extract_title
import os
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # List everything in the content directory
    for entry in os.listdir(dir_path_content):
        # Generate the full path for the current entry
        full_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(full_path):  # Handle files
            # Handle "index.md" specifically
            if entry == "index.md":
                # Define the output path for "index.html"
                output_path = os.path.join(dest_dir_path, "index.html")
            else:
                # Define output path by replacing ".md" with ".html"
                output_path = os.path.join(dest_dir_path, entry).replace(".md", ".html")
            
            print(f"DEBUG: Generating page from {full_path} to {output_path}")
            generate_page(full_path, template_path, output_path)

        elif os.path.isdir(full_path):  # Handle directories
            # Construct the corresponding subdirectory in the destination
            sub_dir_dest = os.path.join(dest_dir_path, entry)
            
            # Ensure the destination subdirectory exists
            os.makedirs(sub_dir_dest, exist_ok=True)
            
            print(f"DEBUG: Recursing into directory: {full_path}")
            # Recursively call function for the subdirectory
            generate_pages_recursive(full_path, template_path, sub_dir_dest)
        
        else:
            print(f"DEBUG: Skipping unknown type: {full_path}")




def generate_page(from_path, template_path, dest_path):
    # Step 1: Print message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    print(f"DEBUG: Attempting to read file at path: {from_path}")

    # Step 2: Read markdown file
    with open(from_path, 'r') as file:
        markdown_content = file.read()

    if not markdown_content.strip():
        raise Exception(f"File at {from_path} is empty or unreadable.")
    print(f"DEBUG: Content of {from_path}:\n{markdown_content}")
    # Step 3: Read template file
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    # Step 4: Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)

    # Assign and THEN debug print it
    html_content = html_node.to_html()
    print(f"DEBUG: Markdown content read from {from_path}:")
    print(markdown_content)
    
    # Step 5: Extract title
    title = extract_title(markdown_content)
    
    # Step 6: Replace placeholders
    html_page = template_content.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_content)
    
    # Step 7: Write output to file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(html_page)



def main():
    # Delete the public directory if it exists
    if os.path.exists("public"):
        shutil.rmtree("public") 
    
    # Copy the 'static' directory to 'public'
    shutil.copytree("static", "public")
    
    print("Static files copied successfully!")
    
    # Generate the index page 
    generate_pages_recursive("content", "template.html", "public")
    print("Page generation completed!") 
# Make sure to call main() at the end of the file
if __name__ == "__main__":
    main()