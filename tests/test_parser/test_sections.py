#!/usr/bin/env python3

#### META: Title: Wallace Section Parser Tests
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: tests/test_parser/test_sections.py

#### SYNOPSIS: Test suite for Wallace section parsing functionality.
#### SYNOPSIS: Validates section start/end tags and nesting behavior.

#### CONTENTS:

import pytest
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError

### SECTION: fixtures
@pytest.fixture
def nested_sections_file(tmp_path):
    file = tmp_path / "nested.py"
    content = '''#### META: Title: Nested Sections Test
#### META: Version: 0.1.1
#### META: PATH: test/nested.py

#### SYNOPSIS: Test file for nested sections.
#### SYNOPSIS: Validates proper section nesting.

#### CONTENTS:

### SECTION: outer
def outer_function():
    pass

### SECTION: inner
def inner_function():
    pass
### END: SECTION: inner

### END: SECTION: outer
'''
    file.write_text(content)
    return str(file)

@pytest.fixture
def mismatched_sections_file(tmp_path):
    file = tmp_path / "mismatched.py"
    content = '''#### META: Title: Mismatched Sections
#### META: Version: 0.1.1

### SECTION: first
def first_function():
    pass
### END: SECTION: second
'''
    file.write_text(content)
    return str(file)

### SECTION: tests
def test_parse_nested_sections(nested_sections_file):
    """Test parsing nested sections."""
    tags = parse_file(nested_sections_file)
    sections = [tag for tag in tags if tag.name in ["SECTION", "END"]]
    assert len(sections) == 4
    
    # Check section pairs match
    section_pairs = zip(sections[::2], sections[1::2])
    for start, end in section_pairs:
        assert start.name == "SECTION"
        assert end.name == "END"
        assert start.content.split(":")[1].strip() == end.content.split(":")[1].strip()

def test_mismatched_sections(mismatched_sections_file):
    """Test error handling for mismatched section tags."""
    with pytest.raises(WallaceError) as exc:
        parse_file(mismatched_sections_file)
    assert "Mismatched section tags" in str(exc.value)

### SECTION: edge_cases
def test_unclosed_section(tmp_path):
    """Test error handling for unclosed sections."""
    file = tmp_path / "unclosed.py"
    content = '''#### META: Title: Unclosed Section
#### META: Version: 0.1.1

### SECTION: unclosed
def unclosed_function():
    pass
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Unclosed section" in str(exc.value)
