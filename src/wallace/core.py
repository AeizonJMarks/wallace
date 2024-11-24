#!/usr/bin/env python3

#### META: Title: Wallace Core
#### META: Version: 0.1.1
#### META: PATH: src/wallace/core.py
#### SYNOPSIS: Minimal core functionality for basic smoke tests
#### CONTENTS:

class WallaceError(Exception):
    """Base exception for Wallace errors."""
    pass

def get_file_style(file_path):
    """Minimal style handling - just returns Python-style prefixes."""
    return {
        'prefix': '#',
        'tag_prefix': '####'
    }
