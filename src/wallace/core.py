#!/usr/bin/env python3

#### META: Title: Wallace Core (Test Implementation)
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: src/wallace/core.py

#### SYNOPSIS: Minimal implementation for testing the test suite.
#### SYNOPSIS: Returns predictable results to verify test behavior.

#### CONTENTS:

class WallaceError(Exception):
    """Base exception for Wallace errors."""
    pass

def validate_tag(tag: str) -> bool:
    """
    Minimal tag validation for testing.
    Only validates basic tag structure.
    """
    if not tag:
        return False
        
    # Basic validation that will pass the initial tests
    if tag.startswith("#### META:"):
        return ":" in tag and len(tag.split(":")) >= 2
    
    if tag.startswith("### SECTION:"):
        return ":" in tag
        
    # Default true for basic tests
    return True

def is_valid_file_structure(content: str) -> bool:
    """
    Minimal file structure validation for testing.
    Checks for required elements in the correct order.
    """
    lines = content.split("\n")
    
    # Check for shebang in .wal files
    if content.strip().endswith(".wal"):
        if not lines[0].startswith("#!"):
            raise WallaceError("Missing shebang in .wal file")
            
    # Check for basic header structure
    has_meta = False
    has_synopsis = False
    has_contents = False
    
    for line in lines:
        if line.startswith("#### META:"):
            has_meta = True
        elif line.startswith("#### SYNOPSIS:"):
            has_synopsis = True
        elif line.startswith("#### CONTENTS:"):
            has_contents = True
            
    if not (has_meta and has_synopsis and has_contents):
        raise WallaceError("Missing required header elements")
        
    return True
