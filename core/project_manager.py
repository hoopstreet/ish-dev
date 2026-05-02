"""This module provides utility functions for managing projects.
"""
import os

def list_projects(project_root='/root/Ai-Coder/projects/'):
    """Lists all folders within the project root directory and checks for a DNA.md file.

    Args:
        project_root (str, optional): The root directory of the projects. Defaults to '/root/Ai-Coder/projects/'.

    Returns:
        list: A list of dictionaries, where each dictionary represents a project folder
              and contains the folder name and a boolean indicating the presence of a DNA.md file.
    """
    projects = []
    if not os.path.exists(project_root):
        return [] # or raise an exception, depends on desired behavior

    for folder_name in os.listdir(project_root):
        folder_path = os.path.join(project_root, folder_name)
        if os.path.isdir(folder_path):
            dna_file_path = os.path.join(folder_path, 'DNA.md')
            has_dna = os.path.exists(dna_file_path)
            projects.append({
                'folder_name': folder_name,
                'has_dna': has_dna
            })
    return projects

if __name__ == '__main__':
    projects = list_projects()
    for project in projects:
        print(f"Project: {project['folder_name']}, DNA.md present: {project['has_dna']}")