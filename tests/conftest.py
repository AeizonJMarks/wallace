#!/usr/bin/env python3

import pytest
import os
import tempfile
from pathlib import Path

@pytest.fixture
def sample_files(tmp_path):
    """Create sample files for testing."""
    # Python file
    py_content = '''#### META: Title: Test
#### META: Version: 0.1.1
#### META: PATH: test/test.py
#### SYNOPSIS: Test file
#### CONTENTS:
'''
    py_file = tmp_path / "test.py"
    py_file.write_text(py_content)
    
    # Wallace file
    wal_content = '''#!/usr/bin/env wallace
#### META: Title: Test
#### META: Version: 0.1.1
#### META: PATH: test/test.wal
#### SYNOPSIS: Test file
#### CONTENTS:
'''
    wal_file = tmp_path / "test.wal"
    wal_file.write_text(wal_content)
    
    return {"python": py_file, "wallace": wal_file}

@pytest.fixture
def mock_file_content():
    """Create mock file content."""
    def _create_content(file_type="py"):
        content = []
        content.append("#### META: Title: Test")
        content.append("#### META: Version: 0.1.1")
        content.append("#### META: PATH: test.py")
        content.append("#### SYNOPSIS: Test file")
        content.append("#### CONTENTS:")
        return "\n".join(content)
    return _create_content

@pytest.fixture 
def file_structure(tmp_path):
    """Create test file structure."""
    src_dir = tmp_path / "src"
    test_dir = tmp_path / "tests"
    src_dir.mkdir()
    test_dir.mkdir()
    
    # Create consistent test content
    test_content = '''#### META: Title: Test
#### META: Version: 0.1.1
#### META: PATH: test.py
#### SYNOPSIS: Test file
#### CONTENTS:
'''
    
    main_file = src_dir / "main.py"
    main_file.write_text(test_content)
    
    test_file = test_dir / "test_main.py"
    test_file.write_text(test_content)
    
    return tmp_path

@pytest.fixture
def temp_file():
    """Create a temporary file."""
    def _create_temp_file(content, suffix='.py'):
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    return _create_temp_file

def pytest_configure(config):
    config.addinivalue_line("markers", "parser: mark test as parser test")
    config.addinivalue_line("markers", "integration: mark test as integration test") 
    config.addinivalue_line("markers", "edge_case: mark test as edge case test")
