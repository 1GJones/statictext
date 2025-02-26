import re
import sys
import os


def extract_title(markdown):
    """
    Extracts the first h1 title from the markdown content.
    
    Args:
        markdown (str): The markdown content to extract the title from.

    Returns:
        str: The extracted title.

    Raises:
        ValueError: If no h1 header is found.
    """
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# ") and not line.startswith("##"):
            if len(line) > 1 and line[1].isspace():
                return line[2:].strip()
    raise ValueError("No h1 title found in the markdown content")

