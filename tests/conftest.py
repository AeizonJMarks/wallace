#!/usr/bin/env python3

#### META: Title: Wallace Test Configuration
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: tests/conftest.py

#### SYNOPSIS: Shared test fixtures and configuration for Wallace test suite.
#### SYNOPSIS: Provides common test data and utilities across all test files.

#### CONTENTS:

import os
import pytest
from pathlib import Path
import tempfile
import shutil

### SECTION: fixtures
@pytest.fixture(scope="session")
def test_files_dir(tmp_path_factory):
    """Create a session-scoped temporary directory for test files."""
    temp_dir = tmp_path_factory.mktemp("wallace_test_files")
    yield temp_dir
    # Cleanup after all tests
    shutil.rmtree(str(temp_dir))

@pytest.fixture
def sample_files(test_files_dir):
    """Create a set of sample files for testing."""
    files = {}
    
    # Python file
    py_content = '''#### META: Title: Sample Python
#### META: Version: 0.1.1
#### META: PATH: test/sample.py

#### SYNOPSIS: Sample test file.
#### CONTENTS:

def test():
    pass
'''
    py_file = test_files_dir / "sample.py"
    py_file.write_text(py_content)
    files["python"] = py_file

    # Wallace file
    wal_content = '''#!/usr/bin/env wallace
#### META: Title: Sample Wallace
#### META: Version: 0.1.1
#### META: PATH: test/sample.wal

#### SYNOPSIS: Sample Wallace file.
#### CONTENTS:

### SECTION: test
### END: SECTION: test
'''
    wal_file = test_files_dir / "sample.wal"
    wal_file.write_text(wal_content)
    files["wallace"] = wal_file

    return files

@pytest.fixture
def mock_file_content():
    """Factory fixture for creating test file content."""
    def _create_content(file_type="py", tags=None):
        """Create file content with specified tags."""
        if tags is None:
            tags = {
                "META": ["Title: Test", "Version: 0.1.1", "PATH: test.py"],
                "SYNOPSIS": ["Test file."],
                "SECTION": ["test"]
            }
            
        content = []
        if file_type == "wal":
            content.append("#!/usr/bin/env wallace")
            
        for tag_type, tag_contents in tags.items():
            for tag_content in tag_contents:
                content.append(f"#### {tag_type}: {tag_content}")
                
        return "\n".join(content)
    
    return _create_content

### SECTION: configuration
def pytest_configure(config):
    """Configure pytest for Wallace testing."""
    # Add wallace markers
    config.addinivalue_line(
        "markers", "parser: mark test as parser test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "edge_case: mark test as edge case test"
    )

@pytest.fixture
def file_structure(test_files_dir):
    """Create a complex file structure for testing."""
    structure = {
        "src": {
            "main.py": '''#### META: Title: Main
#### META: Version: 0.1.1
#### META: PATH: src/main.py

#### SYNOPSIS: Main entry point.
#### CONTENTS:
''',
            "utils": {
                "helpers.py": '''#### META: Title: Helpers
#### META: Version: 0.1.1
#### META: PATH: src/utils/helpers.py

#### SYNOPSIS: Utility functions.
#### CONTENTS:
'''
            }
        },
        "tests": {
            "test_main.py": '''#### META: Title: Main Tests
#### META: Version: 0.1.1
#### META: PATH: tests/test_main.py

#### SYNOPSIS: Test main functionality.
#### CONTENTS:
'''
        }
    }
    
    def create_files(base_path, struct):
        for name, content in struct.items():
            path = base_path / name
            if isinstance(content, dict):
                path.mkdir(exist_ok=True)
                create_files(path, content)
            else:
                path.write_text(content)
    
    create_files(test_files_dir, structure)
    return test_files_dir

@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    def _create_temp_file(content, suffix=".py"):
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    return _create_temp_file
