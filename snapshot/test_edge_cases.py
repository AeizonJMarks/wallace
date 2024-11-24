#!/usr/bin/env python3

#### META: Title: Wallace Edge Case Parser Tests
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: tests/test_parser/test_edge_cases.py

#### SYNOPSIS: Test suite for Wallace parser edge cases.
#### SYNOPSIS: Validates handling of unusual and error conditions.

#### CONTENTS:

import pytest
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError

### SECTION: fixtures
@pytest.fixture
def malformed_meta_file(tmp_path):
    """Create a file with malformed META tags."""
    file = tmp_path / "malformed_meta.py"
    content = '''#### META: Title: Test
#### META:Version: 0.1.1  # Missing space after colon
#### META: PATH test.py   # Missing colon
'''
    file.write_text(content)
    return str(file)

@pytest.fixture
def unicode_file(tmp_path):
    """Create a file with Unicode characters."""
    file = tmp_path / "unicode.py"
    content = '''#### META: Title: Unicode Test 🐍
#### META: Version: 0.1.1
#### META: Author: Test Suite 👩‍💻
#### META: PATH: test/unicode.py

#### SYNOPSIS: Test Unicode handling 📝
#### SYNOPSIS: Including emojis and special chars ⚡️

#### CONTENTS:

### SECTION: code
def test_unicode():
    return "🌟"
### END: SECTION: code'''
    file.write_text(content, encoding='utf-8')
    return str(file)

### SECTION: tests
def test_malformed_meta_tags(malformed_meta_file):
    """Test handling of malformed META tags."""
    with pytest.raises(WallaceError) as exc:
        parse_file(malformed_meta_file)
    assert "Missing required header elements" in str(exc.value)

def test_unicode_handling(unicode_file):
    """Test parsing file with Unicode characters."""
    tags = parse_file(unicode_file)
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert any("🐍" in tag.content for tag in meta_tags)
    assert any("👩‍💻" in tag.content for tag in meta_tags)

def test_whitespace_variants(tmp_path):
    """Test handling of various whitespace patterns."""
    file = tmp_path / "whitespace.py"
    content = '''#### META: Title: Valid Test File
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test.py

#### SYNOPSIS: Test file
#### CONTENTS:

####    META:    Extra    Spaces
####\tMETA:\tUsing\tTabs
####META:NoSpaces
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid tag format" in str(exc.value)

### SECTION: validation_tests
def test_empty_tags(tmp_path):
    """Test handling of empty tag content."""
    file = tmp_path / "empty_tags.py"
    content = '''#### META: Title:
#### META: Version:
#### META: PATH: test.py
#### META: Author: Test

#### SYNOPSIS:
#### CONTENTS:
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Empty tag content" in str(exc.value)

def test_duplicate_meta_tags(tmp_path):
    """Test handling of duplicate META tags."""
    file = tmp_path / "duplicate_meta.py"
    content = '''#### META: Title: First Title
#### META: Title: Second Title
#### META: Version: 0.1.1
#### META: Author: Test
#### META: PATH: test.py

#### SYNOPSIS: Test
#### CONTENTS:
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Duplicate META tag" in str(exc.value)

def test_invalid_characters(tmp_path):
    """Test handling of invalid characters in tags."""
    file = tmp_path / "invalid_chars.py"
    content = '''#### META@: Invalid Character
#### META: Ver$ion: 0.1.1
#### META: Auth*r: Test
#### META: PATH: test.py

#### SYNOPSIS: Test
#### CONTENTS:
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid characters in tag" in str(exc.value)
