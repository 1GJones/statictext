import re


def markdown_to_blocks(markdown):
    ''' Splits a markdown string into a list of block strings, where blocks are 
  separated by one or more empty lines.

  Args:
    markdown: The raw markdown string representing a full document.

  Returns:
    A list of "block" strings.
        - This is another list item
    '''

    # Split the markdown string by one or more occurrences of an empty line 
    # (using a regex that handles different newline types)
    blocks = re.split(r'(?:\r?\n){2,}', markdown.strip())
    
    # Strip whitespace from each block
    blocks = [block.strip() for block in blocks]
    
    #  Filter out any empty blocks
    # blocks = [block for block in blocks if block]
    
    return blocks