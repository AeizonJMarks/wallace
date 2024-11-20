#!/usr/bin/env python3

#### META: Title: Wallace Knowledge Base Snapshot Tool
#### META: Version: 0.1.0
#### META: Author: Claude + Human
#### META: Path: make-snapshot.py
#### TAGS: CLI UTILS

#### SYNOPSIS: Command line tool for creating knowledge base snapshots.
#### SYNOPSIS: Enhanced with selective file type processing capability.
#### SYNOPSIS: Supports prompts-only, python-only, or both file types.

### SECTION: imports
import sys
import shutil
from pathlib import Path
import logging
import argparse

### SECTION: logging_setup
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger('wallace-snapshot')

### SECTION: configuration
# Directories to exclude from snapshot
### FIXME: Tool is picking up wallace-env Python files
### FIXME: Need to exclude virtualenv and other system directories
### DONE: 20/11/2024
EXCLUDE_PATTERNS = [
    'wallace-env',     # Our virtualenv
    'venv',           # Standard virtualenv
    '.env',           # Another common virtualenv
    '__pycache__',    # Python cache directories
    '.pytest_cache',  # Test cache
    'snapshot',       # Our own snapshot directory
    '.git',           # Git directory
    'build',          # Build directories
    'dist',           # Distribution directories
    'egg-info'        # Package info
]

### SECTION: core_functions

### FUNCTION: should_exclude(path: Path) -> bool
### PURE: yes
### EFFECTS: none
def should_exclude(path: Path) -> bool:
    """
    Check if a path should be excluded from the snapshot.
    
    Args:
        path: Path to check
        
    Returns:
        bool: True if path should be excluded
    """
    return any(pattern in str(path) for pattern in EXCLUDE_PATTERNS)

### FUNCTION: create_snapshot(project_root: Path, mode: str) -> None
### PURE: no
### EFFECTS: filesystem read, filesystem write, directory clear
def create_snapshot(project_root: Path, mode: str) -> None:
    """
    Create a fresh snapshot of project files based on specified mode.
    
    Args:
        project_root: Path to the Wallace project root directory
        mode: File types to process ('all', 'prompt', or 'python')
        
    Raises:
        OSError: If filesystem operations fail
        ValueError: If project structure is invalid
    """
    snapshot_dir = project_root / 'snapshot'
    
    # Validate project root
    if not (project_root / '.git').exists():
        raise ValueError(f"Not a git repository: {project_root}")
    
    # Clear/create snapshot directory
    logger.info("Clearing snapshot directory...")
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    snapshot_dir.mkdir()
    
    # Track files and structure
    structure = []
    file_count = 0
    
    # Process Python files if requested
    if mode in ['all', 'python']:
        logger.info("Copying Python files...")
        for file in project_root.rglob('*.py'):
            # Skip excluded directories
            if should_exclude(file):
                continue
            
            # Document structure and copy file
            rel_path = file.relative_to(project_root)
            structure.append(str(rel_path))
            shutil.copy2(file, snapshot_dir / file.name)
            file_count += 1
    
    # Process prompt files if requested
    if mode in ['all', 'prompt']:
        logger.info("Copying prompt files...")
        prompts_dir = project_root / 'prompts'
        if prompts_dir.exists():
            for file in prompts_dir.glob('*.txt'):
                rel_path = file.relative_to(project_root)
                structure.append(str(rel_path))
                shutil.copy2(file, snapshot_dir / file.name)
                file_count += 1
    
    # Write structure documentation
    logger.info("Generating file structure documentation...")
    with open(snapshot_dir / 'file-structure.txt', 'w') as f:
        f.write('\n'.join(sorted(structure)))
    
    # Log completion with mode-specific message
    mode_msg = {'all': 'all files',
               'prompt': 'prompt files only',
               'python': 'Python files only'}
    logger.info(f"Snapshot complete: {file_count} {mode_msg[mode]} processed")

### FUNCTION: main() -> None
### PURE: no
### EFFECTS: argv read, filesystem read, stdout write
def main() -> None:
    """Main entry point for the snapshot tool."""
    parser = argparse.ArgumentParser(
        description='Create Wallace knowledge base snapshot'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--prompt',
        action='store_const',
        dest='mode',
        const='prompt',
        help='process prompt files only'
    )
    group.add_argument(
        '--python',
        action='store_const',
        dest='mode',
        const='python',
        help='process Python files only'
    )
    parser.set_defaults(mode='all')
    
    args = parser.parse_args()
    
    try:
        # Find project root (current or parent directory with .git)
        current = Path.cwd()
        project_root = None
        
        while current != current.parent:
            if (current / '.git').exists():
                project_root = current
                break
            current = current.parent
            
        if not project_root:
            logger.error("Error: Must be run from within a git repository")
            sys.exit(1)
        
        # Create the snapshot
        create_snapshot(project_root, args.mode)
        
    except ValueError as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    except OSError as e:
        logger.error(f"Filesystem error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

### SECTION: entry
if __name__ == '__main__':
    main()
