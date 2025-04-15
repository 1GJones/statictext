import re
def extract_title(markdown):
    """
    Extract the first H1 (# Heading) from the markdown text.
    The H1 must start with exactly one '#' followed by a space.
    """
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown.")
