#!/usr/bin/env python3

#### META: Title: Wallace Core (Smoke Test Version)
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: src/wallace/core.py

#### SYNOPSIS: Core Wallace functionality for smoke tests.
#### SYNOPSIS: Simplified version to get basic tests passing.

#### CONTENTS:

from pathlib import Path
from typing import Dict, Optional, Tuple, List, Union
import os

### SECTION: exceptions
class WallaceError(Exception):
    """Base exception for Wallace errors."""
    pass

### SECTION: file_types
COMMENT_STYLES = {
    '.py': {'prefix': '#', 'tag_prefix': '####', 'section_prefix': '###'},
    '.wal': {'prefix': '#', 'tag_prefix': '####', 'section_prefix': '###'},
    '.txt': {'prefix': '', 'tag_prefix': '', 'section_prefix': ''},
    '.cpp': {'prefix': '//', 'tag_prefix': '////', 'section_prefix': '///'},
    '.css': {'prefix': '/*', 'tag_prefix': '/****', 'section_prefix': '///'},
    '.html': {'prefix': '<!--', 'tag_prefix': '<!--', 'section_prefix': '<!--'}
}

### SECTION: validation
def get_file_style(file_path: Union[str, Path]) -> Dict[str, str]:
    """Get comment style for file type."""
    ext = Path(file_path).suffix.lower()
    try:
        return COMMENT_STYLES[ext]
    except KeyError:
        return COMMENT_STYLES['.py']  # Default to Python style

def strip_comment_markers(line: str, style: Dict[str, str]) -> str:
    """Remove comment markers from line."""
    line = line.strip()
    if not line:
        return ""

    prefix = style['prefix']
    if prefix and line.startswith(prefix):
        line = line[len(prefix):].lstrip()
    return line

def parse_line(line: str, style: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
    """Parse a line into tag type and content."""
    line = line.strip()
    if not line:
        return None, None

    # Handle section tags
    if line.startswith(style['section_prefix']):
        line = line[len(style['section_prefix']):].strip()
        if line.startswith('SECTION:'):
            return 'SECTION', line[8:].strip()
        if line.startswith('END: SECTION:'):
            return 'END', line[12:].strip()
        return None, None

    # Handle regular tags
    if line.startswith(style['tag_prefix']):
        line = line[len(style['tag_prefix']):].strip()
        if ': ' in line:
            tag_type, content = line.split(': ', 1)
            return tag_type, content.strip()

    return None, None

def validate_file_structure(file_path: str, content: str) -> List[str]:
    """Validate basic file structure and return errors."""
    errors = []
    has_meta = False
    has_synopsis = False
    has_contents = False
    style = get_file_style(file_path)
    section_stack = []

    for line in content.splitlines():
        tag_type, _ = parse_line(line, style)
        if tag_type == 'META':
            has_meta = True
        elif tag_type == 'SYNOPSIS':
            has_synopsis = True
        elif tag_type == 'CONTENTS':
            has_contents = True
        elif tag_type == 'SECTION':
            section_stack.append(line)
        elif tag_type == 'END':
            if not section_stack:
                errors.append("END SECTION without matching SECTION")
            else:
                section_stack.pop()

    if not has_meta:
        errors.append("Missing META tags")
    if not has_synopsis:
        errors.append("Missing SYNOPSIS tags")
    if not has_contents:
        errors.append("Missing CONTENTS tag")
    if section_stack:
        errors.append("Unclosed sections")

    return errors

### END: SECTION: validation
