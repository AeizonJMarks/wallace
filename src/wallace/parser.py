#!/usr/bin/env python3

#### META: Title: Wallace Parser
#### META: Version: 0.1.1
#### META: PATH: src/wallace/parser.py
#### SYNOPSIS: Minimal parser implementation for basic smoke tests
#### CONTENTS:

from pathlib import Path
from . import core

class WallaceTag:
    """Represents a parsed Wallace tag."""
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

def parse_file(file_path: str):
    """Basic file parser for smoke tests."""
    # Check file exists
    path = Path(file_path)
    if not path.exists():
        raise core.WallaceError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise core.WallaceError(f"Failed to read file: {str(e)}")

    if not content.strip():
        raise core.WallaceError("Empty file")

    # Get comment style
    style = core.get_file_style(file_path)
    
    # Parse tags
    tags = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
            
        if line.startswith(style['tag_prefix']):
            line = line[len(style['tag_prefix']):].strip()
            if ': ' in line:
                tag_type, content = line.split(': ', 1)
                tags.append(WallaceTag(tag_type.strip(), content.strip()))

    if not tags:
        raise core.WallaceError("No valid Wallace tags found")

    return tags
