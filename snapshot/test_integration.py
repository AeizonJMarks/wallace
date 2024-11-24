#!/usr/bin/env python3

#### META: Title: Wallace Integration Tests
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: tests/test_integration.py

#### SYNOPSIS: Integration test suite for Wallace parser and processing.
#### SYNOPSIS: Tests end-to-end file processing and full spec compliance.
#### SYNOPSIS: Validates interactions between parser, core, and file handling.

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
import tempfile
import shutil
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError
from pathlib import Path

### SECTION: test_structure
@pytest.fixture
def complex_project():
    """Create a complex project structure with multiple file types."""
    temp_dir = tempfile.mkdtemp()
    
    # Create project structure
    os.makedirs(os.path.join(temp_dir, 'src'))
    os.makedirs(os.path.join(temp_dir, 'spec'))
    
    # Python source file
    py_content = '''#!/usr/bin/env python3
#### META: Title: Test Python File
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: src/test.py

#### SYNOPSIS: Complex test file with multiple tags.
#### SYNOPSIS: Tests full Wallace spec compliance.

#### CONTENTS:

### SECTION: imports
import sys

### METRICS: coverage 95% time 120mins

### TODO: Add error handling
### REVIEW: Performance optimization needed
### END: SECTION: imports'''
    
    with open(os.path.join(temp_dir, 'src', 'test.py'), 'w') as f:
        f.write(py_content)

    # Wallace native file
    wal_content = '''#!/usr/bin/env wallace
#### META: Title: Test Wallace File
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: spec/test.wal

#### SYNOPSIS: Native Wallace file format test.
#### SYNOPSIS: Tests specific .wal file requirements.

#### CONTENTS:

### SECTION: definitions
### FUNCTION: process_data(data: list) -> dict

### METRICS: complexity 3 efficiency 85%
### END: SECTION: definitions'''

    with open(os.path.join(temp_dir, 'spec', 'test.wal'), 'w') as f:
        f.write(wal_content)

    yield temp_dir
    shutil.rmtree(temp_dir)

### SECTION: tests
def test_full_project_processing(complex_project):
    """Test processing a complete project structure."""
    py_file = os.path.join(complex_project, 'src', 'test.py')
    wal_file = os.path.join(complex_project, 'spec', 'test.wal')
    
    # Test Python file
    py_tags = parse_file(py_file)
    assert len(py_tags) >= 7  # META, SYNOPSIS, SECTION, METRICS, TODO, REVIEW tags
    
    # Verify all required header elements
    meta_tags = [tag for tag in py_tags if tag.name == "META"]
    assert len(meta_tags) == 4
    
    # Test Wallace native file
    wal_tags = parse_file(wal_file)
    assert len(wal_tags) >= 6  # META, SYNOPSIS, SECTION, FUNCTION, METRICS tags
    assert any(tag.name == "FUNCTION" for tag in wal_tags)

def test_cross_references(tmp_path):
    """Test handling of cross-references between files."""
    content = '''#### META: Title: Cross Reference Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: src/test.py

#### SYNOPSIS: Tests cross-references.
#### CONTENTS:

### SECTION: core
### LINK: ./utils/helpers.py:123#process_data
### LINK: ../specs/protocol.wal#validation
### END: SECTION: core'''

    file = tmp_path / "test.py"
    file.write_text(content)
    
    tags = parse_file(str(file))
    links = [tag for tag in tags if tag.name == "LINK"]
    assert len(links) == 2
    assert all("#" in link.content for link in links)

def test_metrics_validation(tmp_path):
    """Test metrics tag validation."""
    content = '''#### META: Title: Metrics Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test.py

#### SYNOPSIS: Tests metrics validation.
#### CONTENTS:

### SECTION: performance
### METRICS: coverage 95% complexity 3 time 45mins
### METRICS: $50 £30 €40
### END: SECTION: performance'''

    file = tmp_path / "test.py"
    file.write_text(content)
    
    tags = parse_file(str(file))
    metrics = [tag for tag in tags if tag.name == "METRICS"]
    assert len(metrics) == 2

def test_file_order_requirements(tmp_path):
    """Test strict ordering requirements from EBNF spec."""
    # Test shebang before headerBlock requirement
    content = '''#### META: Title: Wrong Order
#!/usr/bin/env wallace
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test.wal

#### SYNOPSIS: Test file order.
#### CONTENTS:'''

    file = tmp_path / "invalid_order.wal"
    file.write_text(content)
    
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid file structure" in str(exc.value)

def test_comment_block_interaction(tmp_path):
    """Test comment block parsing according to EBNF spec."""
    content = '''#!/usr/bin/env python3
/* #### META: Title: Test */ 
#### META: Title: Real Title
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test.py

#### SYNOPSIS: Test comment blocks.
#### CONTENTS:'''

    file = tmp_path / "comment_test.py"
    file.write_text(content)
    
    tags = parse_file(str(file))
    meta_tags = [tag for tag in tags if tag.name == "META"]
    assert len(meta_tags) == 4
    titles = [tag.content for tag in meta_tags if "Title:" in tag.content]
    assert len(titles) == 1
    assert "Real Title" in titles[0]

### SECTION: validation
def test_strict_ebnf_compliance(tmp_path):
    """Test strict compliance with EBNF grammar specification."""
    content = '''#### META: Title: EBNF Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test.py

#### SYNOPSIS: Tests EBNF compliance.
#### CONTENTS:

### SECTION: test
#### TODO: Test task
#### DONE: 12/31/2023 15:30
#### FIXME: Important fix
#### IDEA: New feature
#### REVIEW: Code review
#### NOTE: Important note
#### TRIAGE: Priority task
### END: SECTION: test'''

    file = tmp_path / "test.py"
    file.write_text(content)
    
    tags = parse_file(str(file))
    tag_names = {tag.name for tag in tags}
    required_tags = {"TODO", "DONE", "FIXME", "IDEA", "REVIEW", "NOTE", "TRIAGE"}
    assert required_tags.issubset(tag_names)

def test_reference_format_validation(tmp_path):
    """Test validation of reference formats in tags."""
    content = '''#### META: Title: Reference Test
#### META: Version: 0.1.1
#### META: Author: Test Suite
#### META: PATH: test.py

#### SYNOPSIS: Tests references.
#### CONTENTS:

### SECTION: test
### LINK: ./src/file.py:123#function
### LINK: ../invalid:.py#wrong
### END: SECTION: test'''

    file = tmp_path / "test.py"
    file.write_text(content)
    
    with pytest.raises(WallaceError) as exc:
        parse_file(str(file))
    assert "Invalid reference format" in str(exc.value)
