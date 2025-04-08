import re

from enum import Enum

class BlockType(Enum):
      
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
     '''
      Detects the block type based on its content.
      
      Args: 
          block: A markdown text as input
      
      Returns: 
             The BlockType representing the type of block it is 
    
     '''
    
    
     # Check for headings 
     if re.match(r"^#+\s",block): # Heading starts with one or more '#' followed by a space.
         return BlockType.HEADING
    
    # Check for code blocks 
     if re.match(r"^```", block) or re.match(r"^( {4}|\t)", block, re.MULTILINE):# Code block starts with ``` or indented by at least four spaces or a tab.
        return BlockType.CODE
    
    
     # Check for quote blocks
     if re.match(r"^>\s", block):
         return BlockType.QUOTE
     
      # Check for unordered list
     if re.match(r"^[-*+]\s", block):
          return BlockType.UNORDERED_LIST
      
       # Check for ordered list
     if re.match(r"^\d+\.\s", block):
         return BlockType.ORDERED_LIST
     
     return BlockType.PARAGRAPH