#!/usr/bin/env python3

#### META: Title: Wallace Section Parser Tests
#### META: Version: 0.1.1
#### META: Author: Test Suite
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
    """Create a file with nested sections."""
    file = tmp_path / "nested.py"
    content = '''#### META: Title: Nested Sections Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
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
    """Create a file with mismatched section tags."""
    file = tmp_path / "mismatched.py"
    content = '''#### META: Title: Mismatched Sections
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test/mismatched.py

#### SYNOPSIS: Test mismatched section tags.
#### CONTENTS:

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
    section_stack = []
    for tag in sections:
        if tag.name == "SECTION":
            section_stack.append(tag.content)
        else:  # END tag
            assert tag.content == section_stack.pop()
    assert len(section_stack) == 0

def test_mismatched_sections(mismatched_sections_file):
    """Test error handling for mismatched section tags."""
    with pytest.raises(WallaceError) as exc:
        parse_file(mismatched_sections_file)
    assert "Mismatched section tags" in str(exc.value)

def test_unclosed_section(tmp_path):
    """Test error handling for unclosed sections."""
    file = tmp_path / "unclosed.py"
    content = '''#### META: Title: Unclosed Section Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test/unclosed.py

#### SYNOPSIS: Test unclosed sections.
#### CONTENTS:

### SECTION: unclosed
def unclosed_function():
    pass
# Missing END tag
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Unclosed section" in str(exc.value)

### SECTION: validation_tests
def test_empty_section(tmp_path):
    """Test handling of empty sections."""
    file = tmp_path / "empty_section.py"
    content = '''#### META: Title: Empty Section Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test/empty.py

#### SYNOPSIS: Test empty sections.
#### CONTENTS:

### SECTION: empty
### END: SECTION: empty
'''
    file.write_text(content)
    tags = parse_file(str(file))
    sections = [tag for tag in tags if tag.name in ["SECTION", "END"]]
    assert len(sections) == 2
    assert sections[0].content == sections[1].content == "empty"

def test_nested_content(tmp_path):
    """Test content within nested sections."""
    file = tmp_path / "nested_content.py"
    content = '''#### META: Title: Nested Content Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test/nested_content.py

#### SYNOPSIS: Test nested section content.
#### CONTENTS:

### SECTION: outer
#### TODO: Outer task

    ### SECTION: inner
    #### TODO: Inner task
    ### END: SECTION: inner

### END: SECTION: outer
'''
    file.write_text(content)
    tags = parse_file(str(file))
    todos = [tag for tag in tags if tag.name == "TODO"]
    assert len(todos) == 2
    assert "Outer task" in todos[0].content
    assert "Inner task" in todos[1].content
