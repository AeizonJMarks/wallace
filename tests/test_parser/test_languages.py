#!/usr/bin/env python3

#### META: Title: Wallace Language-Specific Parser Tests
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: tests/test_parser/test_languages.py

#### SYNOPSIS: Test suite for language-specific Wallace parsing.
#### SYNOPSIS: Validates comment syntax and tag handling across languages.

#### CONTENTS:

import pytest
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError

### SECTION: fixtures
@pytest.fixture
def python_file(tmp_path):
    """Create a Python test file."""
    file = tmp_path / "test.py"
    content = '''#!/usr/bin/env python3

#### META: Title: Python Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test/test.py

#### SYNOPSIS: Python file with Wallace tags.
#### SYNOPSIS: Tests Python-style comments.

#### CONTENTS:

### SECTION: code
def test_function():
    pass
### END: SECTION: code
'''
    file.write_text(content)
    return str(file)

@pytest.fixture
def cpp_file(tmp_path):
    """Create a C++ test file."""
    file = tmp_path / "test.cpp"
    content = '''//// META: Title: C++ Test
//// META: Version: 0.1.1
//// META: Author: Test Suite
//// META: PATH: test/test.cpp

//// SYNOPSIS: C++ file with Wallace tags.
//// SYNOPSIS: Tests C++-style comments.

//// CONTENTS:

/// SECTION: code
int main() {
    return 0;
}
/// END: SECTION: code
'''
    file.write_text(content)
    return str(file)

@pytest.fixture
def css_file(tmp_path):
    """Create a CSS test file."""
    file = tmp_path / "test.css"
    content = '''/***** META: Title: CSS Test
***** META: Version: 0.1.1
***** META: Author: Test Suite
***** META: PATH: test/test.css

***** SYNOPSIS: CSS file with Wallace tags.
***** SYNOPSIS: Tests CSS-style comments.

***** CONTENTS:

*** SECTION: styles */
body {
    margin: 0;
}
/* *** END: SECTION: styles */
'''
    file.write_text(content)
    return str(file)

@pytest.fixture
def html_file(tmp_path):
    """Create an HTML test file."""
    file = tmp_path / "test.html"
    content = '''<!-- META: Title: HTML Test -->
<!-- META: Version: 0.1.1 -->
<!-- META: Author: Test Suite -->
<!-- META: PATH: test/test.html -->

<!-- SYNOPSIS: HTML file with Wallace tags. -->
<!-- SYNOPSIS: Tests HTML-style comments. -->

<!-- CONTENTS: -->

<!-- SECTION: body -->
<body>
    <h1>Test</h1>
</body>
<!-- END: SECTION: body -->
'''
    file.write_text(content)
    return str(file)

### SECTION: tests
def test_python_parsing(python_file):
    """Test parsing Python-style Wallace tags."""
    tags = parse_file(python_file)
    assert len(tags) >= 6  # META, SYNOPSIS, SECTION tags
    
    # Verify prefix handling
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4
    assert all(tag.content.strip().startswith(("Title:", "Version:", "Author:", "PATH:")) 
              for tag in meta_tags)
    
    # Check section tags use correct prefix
    section_tags = [tag for tag in tags if tag.name in ["SECTION", "END"]]
    assert len(section_tags) == 2

def test_cpp_parsing(cpp_file):
    """Test parsing C++-style Wallace tags."""
    tags = parse_file(cpp_file)
    assert len(tags) >= 6
    
    # Verify prefix handling
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4
    assert all(tag.content.strip().startswith(("Title:", "Version:", "Author:", "PATH:"))
              for tag in meta_tags)

def test_html_parsing(html_file):
    """Test parsing HTML-style Wallace tags."""
    tags = parse_file(html_file)
    assert len(tags) >= 6
    
    # Verify HTML comment style doesn't affect tag content
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4
    assert all(tag.content.strip().startswith(("Title:", "Version:", "Author:", "PATH:"))
              for tag in meta_tags)

def test_css_parsing(css_file):
    """Test parsing CSS-style Wallace tags."""
    tags = parse_file(css_file)
    assert len(tags) >= 6
    
    # Verify CSS comment style doesn't affect tag content
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4
    assert all(tag.content.strip().startswith(("Title:", "Version:", "Author:", "PATH:"))
              for tag in meta_tags)

### SECTION: error_tests
def test_mixed_comment_styles(tmp_path):
    """Test handling of mixed comment styles in a single file."""
    file = tmp_path / "mixed.txt"
    content = '''#### META: Title: Mixed Comments
// META: Version: 0.1.1
<!-- META: PATH: test/mixed.txt -->

#### SYNOPSIS: Tests mixed comment styles.
#### CONTENTS:
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid comment style" in str(exc.value)

def test_invalid_comment_style(tmp_path):
    """Test handling of invalid comment style for file type."""
    file = tmp_path / "invalid.py"
    content = '''// META: Title: Wrong Style
// META: Version: 0.1.1
// META: Author: Test
// META: PATH: test.py

// SYNOPSIS: Test
// CONTENTS:
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid comment style" in str(exc.value)
