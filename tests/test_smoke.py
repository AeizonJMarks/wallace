#!/usr/bin/env python3

#### META: Title: Wallace Smoke Tests
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: tests/test_smoke.py

#### SYNOPSIS: Smoke tests to verify test suite functionality.
#### SYNOPSIS: Tests basic assumptions and fixture behavior.

#### CONTENTS:

import pytest
from wallace.parser import parse_file, WallaceTag
from wallace.core import WallaceError
import os

### SECTION: fixture_tests
def test_sample_files_fixture(sample_files):
    """Verify the sample_files fixture creates valid files."""
    assert "python" in sample_files
    assert "wallace" in sample_files
    assert sample_files["python"].exists()
    assert sample_files["wallace"].exists()

def test_mock_file_content_fixture(mock_file_content):
    """Verify the mock_file_content fixture produces valid content."""
    content = mock_file_content()
    assert "#### META: Title:" in content
    assert "#### SYNOPSIS:" in content

def test_file_structure_fixture(file_structure):
    """Verify the file_structure fixture creates correct hierarchy."""
    assert (file_structure / "src").exists()
    assert (file_structure / "src" / "main.py").exists()
    assert (file_structure / "tests").exists()

### SECTION: parser_tests
def test_basic_parsing(sample_files):
    """Verify basic parsing functionality works."""
    py_file = sample_files["python"]
    tags = parse_file(str(py_file))
    assert len(tags) > 0
    assert all(isinstance(tag, WallaceTag) for tag in tags)

def test_error_handling(temp_file):
    """Verify error handling behavior."""
    # Test missing file
    with pytest.raises(WallaceError) as exc:
        parse_file("nonexistent.py")
    assert "File not found" in str(exc.value)
    
    # Test invalid content
    invalid_content = "Invalid content without proper tags"
    path = temp_file(invalid_content)
    with pytest.raises(WallaceError):
        parse_file(path)
    os.unlink(path)  # Cleanup

### SECTION: integration_tests
def test_full_workflow(file_structure):
    """Verify complete workflow using all fixtures."""
    main_py = file_structure / "src" / "main.py"
    helper_py = file_structure / "src" / "utils" / "helpers.py"
    test_py = file_structure / "tests" / "test_main.py"
    
    # All files should be parseable
    for file in [main_py, helper_py, test_py]:
        tags = parse_file(str(file))
        assert len(tags) > 0
        
        # Verify required tags
        tag_names = [tag.name for tag in tags]
        assert "META" in tag_names
        assert "SYNOPSIS" in tag_names

### SECTION: marker_tests
@pytest.mark.parser
def test_parser_marker():
    """Verify parser marker is registered."""
    pass

@pytest.mark.integration
def test_integration_marker():
    """Verify integration marker is registered."""
    pass

@pytest.mark.edge_case
def test_edge_case_marker():
    """Verify edge_case marker is registered."""
    pass
