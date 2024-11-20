#!/usr/bin/env python3

#### META: PATH: src/wallace/core.py
class WallaceError(Exception):
    """Base exception for Wallace errors."""
    pass

def validate_tag(tag: str) -> bool:
    """Validate a Wallace tag."""
    # Basic validation for now
    return True
