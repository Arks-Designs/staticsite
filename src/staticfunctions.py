"""Module for functions related to generation of static site"""
import os
import shutil

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
