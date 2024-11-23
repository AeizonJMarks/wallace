#!/usr/bin/env python3

#### META: Title: Wallace Integration Tests
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: tests/test_integration.py

#### SYNOPSIS: Integration test suite for Wallace parser and processing.
#### SYNOPSIS: Tests end-to-end file processing and full spec compliance.
#### SYNOPSIS: Validates interactions between parser, core, and file handling.
#### SYNOPSIS: Includes comprehensive validation against EBNF grammar spec.

#### CONTENTS:

### FIXME: EBNF spec has ambiguous handling of nested tags within comment blocks
###        Need to clarify if Wallace tags inside comment blocks should be parsed
###        See wallaceLine definition in EBNF

### TRIAGE: Priority 1 - Edge cases from EBNF review:
###         1. Handling of shebang + headerBlock order in sourceFile
###         2. commentBlock interaction with metaBlock
###         3. Validation of currency symbols in metricValue
###         4. Path reference format validation

import os
import pytest
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError
import tempfile
import shutil

### SECTION: fixtures
@pytest.fixture
def test_dir():
    """Create a temporary test directory with multiple test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def complex_project(test_dir):
    """Create a complex project structure with multiple file types."""
    # Python source file
    py_content = '''#!/usr/bin/env python3
#### META: Title: Test Python File
#### META: Version: 0.1.1
#### META: PATH: src/test.py

#### SYNOPSIS: Complex test file with multiple tags.
#### SYNOPSIS: Tests full Wallace spec compliance.

#### CONTENTS:

### SECTION: imports @0.1.1
import sys

### SECTION: code
def main():
    pass
### END: SECTION: code

### METRICS: coverage 95% time 120mins

### TODO: Add error handling
### REVIEW: Performance optimization needed
### END: SECTION: imports
'''
    os.makedirs(os.path.join(test_dir, 'src'))
    with open(os.path.join(test_dir, 'src', 'test.py'), 'w') as f:
        f.write(py_content)

    # Wallace native file
    wal_content = '''#!/usr/bin/env wallace
#### META: Title: Test Wallace File
#### META: Version: 0.1.1
#### META: PATH: spec/test.wal

#### SYNOPSIS: Native Wallace file format test.
#### SYNOPSIS: Tests specific .wal file requirements.

#### CONTENTS:

### SECTION: definitions
### FUNCTION: process_data(data: list) -> dict

### METRICS: complexity 3 efficiency 85%
### END: SECTION: definitions
'''
    os.makedirs(os.path.join(test_dir, 'spec'))
    with open(os.path.join(test_dir, 'spec', 'test.wal'), 'w') as f:
        f.write(wal_content)
    
    return test_dir

### SECTION: tests
def test_full_project_processing(complex_project):
    """Test processing a complete project structure."""
    py_file = os.path.join(complex_project, 'src', 'test.py')
    wal_file = os.path.join(complex_project, 'spec', 'test.wal')
    
    # Test Python file
    py_tags = parse_file(py_file)
    assert len(py_tags) >= 8  # META, SYNOPSIS, SECTION, METRICS, TODO, REVIEW tags
    
    # Verify all required header elements
    meta_tags = [tag for tag in py_tags if tag.name == "META"]
    assert len(meta_tags) == 3
    assert any(tag.content.startswith("Title:") for tag in meta_tags)
    assert any(tag.content.startswith("Version:") for tag in meta_tags)
    assert any(tag.content.startswith("PATH:") for tag in meta_tags)
    
    # Test Wallace native file
    wal_tags = parse_file(wal_file)
    assert len(wal_tags) >= 6  # META, SYNOPSIS, SECTION, FUNCTION, METRICS tags

def test_cross_references(complex_project):
    """Test handling of cross-references between files."""
    py_file = os.path.join(complex_project, 'src', 'test.py')
    
    tags = parse_file(py_file)
    section_tags = [tag for tag in tags if tag.name == "SECTION"]
    
    # Check section versioning format
    assert any("@0.1.1" in tag.content for tag in section_tags)

def test_metrics_validation(complex_project):
    """Test parsing and validation of METRICS tags."""
    py_file = os.path.join(complex_project, 'src', 'test.py')
    wal_file = os.path.join(complex_project, 'spec', 'test.wal')
    
    py_tags = parse_file(py_file)
    wal_tags = parse_file(wal_file)
    
    # Check different METRICS formats
    py_metrics = [tag for tag in py_tags if tag.name == "METRICS"][0]
    assert "%" in py_metrics.content  # Percentage format
    assert "mins" in py_metrics.content  # Time unit
    
    wal_metrics = [tag for tag in wal_tags if tag.name == "METRICS"][0]
    assert any(char.isdigit() for char in wal_metrics.content)  # Numeric value

### SECTION: edge_cases
def test_file_order_requirements(tmp_path):
    """Test strict ordering requirements from EBNF spec."""
    file = tmp_path / "order_test.wal"
    
    # Test shebang before headerBlock requirement
    content = '''#### META: Title: Wrong Order
#!/usr/bin/env wallace
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid file structure" in str(exc.value)

def test_comment_block_interaction(tmp_path):
    """Test comment block parsing according to EBNF spec."""
    file = tmp_path / "comment_test.py"
    content = '''#!/usr/bin/env python3
/* 
#### META: Title: Test
*/
#### META: Version: 0.1.1
'''
    file.write_text(content)
    # This should validate according to final EBNF clarification
    tags = parse_file(str(file))
    assert len(tags) > 0

### SECTION: validation
def test_strict_ebnf_compliance(complex_project):
    """Test strict compliance with EBNF grammar specification."""
    py_file = os.path.join(complex_project, 'src', 'test.py')
    tags = parse_file(py_file)
    
    # Validate shebang format
    with open(py_file, 'r') as f:
        first_line = f.readline().strip()
    assert first_line.startswith("#!")
    
    # Validate tag level formatting
    for tag in tags:
        if tag.name == "META":
            # Validate META tag format according to EBNF
            assert ":" in tag.content
            key, value = tag.content.split(":", 1)
            assert key.strip().isupper()
            assert value.strip()

def test_reference_format_validation(tmp_path):
    """Test validation of reference formats in tags."""
    file = tmp_path / "reference_test.py"
    content = '''#### META: Title: Reference Test
#### META: Version: 0.1.1
#### META: PATH: test.py

### LINK: ./src/file.py:123#function
### LINK: ../invalid:.py#wrong
'''
    file.write_text(content)
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid reference format" in str(exc.value)
