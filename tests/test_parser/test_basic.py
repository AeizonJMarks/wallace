#!/usr/bin/env python3

#### META: Title: Wallace Basic Parser Tests
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: tests/test_parser/test_basic.py

#### SYNOPSIS: Basic test suite for Wallace parser functionality.
#### SYNOPSIS: Tests fundamental parsing capabilities and basic tag validation.

#### CONTENTS:

import pytest
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError

### SECTION: fixtures
@pytest.fixture
def valid_python_file(tmp_path):
    file = tmp_path / "valid.py"
    content = '''#### META: Title: Test File
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test/valid.py

#### SYNOPSIS: Test file for basic parsing.
#### SYNOPSIS: Contains valid Wallace tags.

#### CONTENTS:

### SECTION: code
def test_function():
    pass
### END: SECTION: code
'''
    file.write_text(content)
    return str(file)

@pytest.fixture
def invalid_python_file(tmp_path):
    file = tmp_path / "invalid.py"
    content = '''#META: Missing space
# meta: Lowercase
# META:Missing space
'''
    file.write_text(content)
    return str(file)

### SECTION: tests
def test_parse_valid_file(valid_python_file):
    """Test parsing a valid Python file with Wallace tags."""
    tags = parse_file(valid_python_file)
    assert len(tags) == 7
    assert all(isinstance(tag, WallaceTag) for tag in tags)
    
    # Check META tags
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4
    assert any(tag.content.startswith("Title:") for tag in meta_tags)
    
    # Check SYNOPSIS tags
    synopsis_tags = [tag for tag in tags if tag.name == "SYNOPSIS"]
    assert len(synopsis_tags) == 2

def test_parse_invalid_file(invalid_python_file):
    """Test parsing a file with invalid Wallace tags."""
    with pytest.raises(WallaceError):
        parse_file(invalid_python_file)

def test_missing_file():
    """Test attempting to parse a non-existent file."""
    with pytest.raises(WallaceError) as exc:
        parse_file("nonexistent.py")
    assert "File not found" in str(exc.value)

### SECTION: edge_cases
def test_empty_file(tmp_path):
    """Test parsing an empty file."""
    file = tmp_path / "empty.py"
    file.write_text("")
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "No valid Wallace tags found" in str(exc.value)
