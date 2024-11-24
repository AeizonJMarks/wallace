#!/usr/bin/env python3

#### META: Title: Wallace Basic Parser Tests
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: tests/test_parser/test_basic.py

#### SYNOPSIS: Basic test suite for Wallace parser functionality.
#### SYNOPSIS: Tests fundamental parsing capabilities and tag validation.

#### CONTENTS:

import pytest
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError
from pathlib import Path

### SECTION: fixtures
@pytest.fixture
def valid_python_file(tmp_path):
    """Create a valid Python test file."""
    file = tmp_path / "valid.py"
    content = '''#!/usr/bin/env python3

#### META: Title: Valid Python Test File
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: tests/test_files/python/valid.py

#### SYNOPSIS: Test file for Python parsing.
#### SYNOPSIS: Contains valid Wallace tags.
#### SYNOPSIS: Used in basic parsing tests.

#### CONTENTS:

### SECTION: code
def test_function():
    """Test function for demonstration."""
    pass
### END: SECTION: code'''
    file.write_text(content)
    return str(file)

@pytest.fixture
def invalid_python_file(tmp_path):
    """Create an invalid Python test file."""
    file = tmp_path / "invalid.py"
    content = '''# Invalid META tag format
####META:Title:Missing Spaces
#### meta: Lowercase Tag Name
#### META:Missing space after colon:Value'''
    file.write_text(content)
    return str(file)

### SECTION: tests
def test_parse_valid_file(valid_python_file):
    """Test parsing a valid Python file with Wallace tags."""
    tags = parse_file(valid_python_file)
    assert len(tags) >= 6  # META, SYNOPSIS, SECTION tags
    
    # Check META tags
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4
    titles = [tag.content for tag in meta_tags if "Title:" in tag.content]
    assert len(titles) == 1
    assert "Valid Python Test File" in titles[0]
    
    # Check SYNOPSIS tags
    synopsis_tags = [tag for tag in tags if tag.name == "SYNOPSIS"]
    assert len(synopsis_tags) == 3

    # Check SECTION tags
    section_tags = [tag for tag in tags if tag.name in ["SECTION", "END"]]
    assert len(section_tags) == 2
    assert section_tags[0].content == "code"
    assert section_tags[1].content == "code"

def test_parse_invalid_file(invalid_python_file):
    """Test parsing a file with invalid Wallace tags."""
    with pytest.raises(WallaceError) as exc:
        parse_file(invalid_python_file)
    assert "Missing required header elements" in str(exc.value)

def test_missing_file():
    """Test attempting to parse a non-existent file."""
    with pytest.raises(WallaceError) as exc:
        parse_file("nonexistent.py")
    assert "File not found" in str(exc.value)

def test_empty_file(tmp_path):
    """Test parsing an empty file."""
    file = tmp_path / "empty.py"
    file.write_text("")
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Missing required header elements" in str(exc.value)

### SECTION: validation_tests
def test_validate_meta_tags(tmp_path):
    """Test validation of META tags."""
    file = tmp_path / "meta_tags.py"
    content = '''#### META: Title: Test
#### META: Version: 0.1.1
#### META: Author: Test
#### META: PATH: test.py

#### SYNOPSIS: Test
#### CONTENTS:
'''
    file.write_text(content)
    tags = parse_file(str(file))
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4

def test_validate_synopsis_tags(tmp_path):
    """Test validation of SYNOPSIS tags."""
    file = tmp_path / "synopsis_tags.py"
    content = '''#### META: Title: Test
#### META: Version: 0.1.1
#### META: Author: Test
#### META: PATH: test.py

#### SYNOPSIS: First line
#### SYNOPSIS: Second line
#### SYNOPSIS: Third line

#### CONTENTS:
'''
    file.write_text(content)
    tags = parse_file(str(file))
    synopsis_tags = [tag for tag in tags if tag.name == "SYNOPSIS"]
    assert len(synopsis_tags) == 3
