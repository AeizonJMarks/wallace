#!/usr/bin/env python3

#### META: Title: Test Setup
#### META: Version: 0.1.0-alpha

# tests/test_core.py
#### META: PATH: tests/test_core.py
import pytest
from wallace import core

def test_validate_tag():
    """Test basic tag validation."""
    assert core.validate_tag("#### META: Test")
