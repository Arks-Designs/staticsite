"""Module for functions related to generation of static site"""
import os
import shutil
from textfunctions import markdown_to_html_node, extract_title

def copy_from_static_to_public(source:str, dest:str)->None:
    # Get targets for source and destination
    cwd = os.getcwd()
    source = os.path.join(cwd, source)
    dest = os.path.join(cwd, dest)
    if not os.path.exists(source):
        raise ValueError("Source is not present")
    #print(source, dest)

    # Delete contents of destination
    shutil.rmtree(dest, ignore_errors=True)

    # Recreate destination
    os.mkdir(dest)

    # Get contents of source
    children = os.listdir(source)

    # Copy or create contents based on whether dir or file
    for child in children:
        child_full_path = os.path.join(source, child)
        if os.path.isfile(child_full_path):
            shutil.copy(child_full_path, dest)
        else:
            copy_from_static_to_public(child_full_path, os.path.join(dest, child))

def generate_page(from_path:str, template_path:str, dest_path:str)->None:
    """Method to create a page for our site"""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        input_markdown = file.read()
    with open(template_path) as file:
        template_html = file.read()
    

    html_node = markdown_to_html_node(input_markdown)
    #print(html_node)
    html_str = html_node.to_html()

    title = extract_title(input_markdown)

    updated_html = template_html.replace("{{ Title }}", title)
    updated_html = updated_html.replace("{{ Content }}", html_str)

    #print(updated_html)
    cwd = os.getcwd()
    remaining_dest = dest_path.split(cwd)[1].split("/")
    remaining_dirs = remaining_dest[:-1]
    print(remaining_dirs)
    file_name = remaining_dest[-1]
    for directory in remaining_dirs:
        cwd = os.path.join(cwd, directory)
        if not os.path.exists(cwd):
            os.mkdir(cwd)

    with open(os.path.join(cwd, file_name), "w") as file:
        file.write(updated_html)

def generate_pages_recursive(dir_path_content:str, template_path:str, dest_dir_path:str)->None:
    """Method to generate all pages from content as html pages"""
    content_files = os.listdir(dir_path_content)
    for file in content_files:
        content_file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(content_file_path):
            dest_file_path = dest_file_path.replace(".md", ".html")
            generate_page(content_file_path, template_path, dest_file_path)
        else:
            generate_pages_recursive(content_file_path, template_path, dest_file_path)
