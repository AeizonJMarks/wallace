#!/usr/bin/env python3

#### META: Title: Wallace Command Line Tool
#### META: Version: 0.1.0
#### META: Author: Claude + Human
#### META: Path: ~/wallace/wallace.py
#### TAGS: MANUAL COMMANDS

#### VERSION: 0.1.0 @alpha #abc123

#### SYNOPSIS: Core Wallace command line tool.
#### SYNOPSIS: Provides unified interface for Wallace operations.
#### SYNOPSIS: Currently implements parse subcommand.

#### MANUAL: NAME
####        wallace - Wallace development tool
####
#### MANUAL: SYNOPSIS
####        wallace <command> [options] [arguments]
####
#### MANUAL: DESCRIPTION
####        Command line interface for Wallace development system.
####        Manages Wallace tags and operations across codebases.
####
#### MANUAL: COMMANDS
####        parse       Validate Wallace tag syntax
####        help       Display general help or command-specific help
####
#### MANUAL: OPTIONS
####        -h, --help     Show this help message
####        -v, --version  Show version information

### SECTION: imports @0.1.0
import sys
import argparse
import re
from pathlib import Path

### SECTION: configuration @0.1.0
# Wallace tag patterns
WALLACE_PATTERNS = {
    'TAG_TXT': r'^[A-Z]+:\s|^\s[A-Z]+:\s',         # For .txt files
    'TAG_OTHER': r'^\s*[#;]+\s+[A-Z]+:\s'          # For commented files
}

### FUNCTION: parse_content(content: str, is_txt: bool) -> list
### PURE: yes
### EFFECTS: none
def parse_content(content: str, is_txt: bool) -> list:
    """Parse content for Wallace tags and return matches."""
    pattern = WALLACE_PATTERNS['TAG_TXT'] if is_txt else WALLACE_PATTERNS['TAG_OTHER']
    matches = []
    
    # Find all matches in content
    for i, line in enumerate(content.splitlines(), 1):
        for match in re.finditer(pattern, line):
            tag = match.group().strip()
            # Remove comment chars for non-txt files
            if not is_txt:
                tag = re.sub(r'^[#;]+\s+', '', tag)
            matches.append({
                'line': i,
                'position': match.start(),
                'tag': tag
            })
    
    return matches

### FUNCTION: process_file(file_path: str) -> None
### PURE: no
### EFFECTS: filesystem read, stdout write
def process_file(file_path: str) -> None:
    """Process a file and display found tags."""
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"wallace: error: file '{file_path}' does not exist")
            sys.exit(1)
            
        is_txt = path.suffix == '.txt'
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        matches = parse_content(content, is_txt)
        display_results(matches, file_path)
        
    except Exception as e:
        print(f"wallace: error: {str(e)}")
        sys.exit(1)

### FUNCTION: display_results(matches: list, source: str) -> None
### PURE: no
### EFFECTS: stdout write
def display_results(matches: list, source: str) -> None:
    """Display parsing results."""
    print(f"Analyzing {source}:")
    if not matches:
        print("No Wallace tags found.")
        return
    
    print(f"Found {len(matches)} tags:")
    for match in matches:
        print(f"Line {match['line']}, Pos {match['position']}: {match['tag']}")

### FUNCTION: show_main_help() -> None
### PURE: no
### EFFECTS: stdout write
def show_main_help() -> None:
    """Display main Wallace help message."""
    print("""usage: wallace [-h] [-v] {parse} ...

Wallace development tool

commands:
  parse         validate Wallace tag syntax

optional arguments:
  -h, --help    show this help message and exit
  -v, --version show program version""")

### FUNCTION: show_parse_help() -> None
### PURE: no
### EFFECTS: stdout write
def show_parse_help() -> None:
    """Display parse command help message."""
    print("""usage: wallace parse [-h] file

Validate Wallace tag syntax in files

positional arguments:
  file        file to parse

optional arguments:
  -h, --help  show this help message and exit

examples:
  wallace parse myfile.txt    parse a text file
  wallace parse script.py     parse a Python file
  wallace parse config.el     parse an Elisp file

file type handling:
  .txt files:  tags may start at line beginning
  other files: tags must follow language comment syntax""")

### FUNCTION: main() -> None
### PURE: no
### EFFECTS: argv read, filesystem read, stdout write
def main() -> None:
    """Main entry point for Wallace command line tool."""
    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        show_main_help()
        sys.exit(0)
        
    if sys.argv[1] in ['-v', '--version']:
        print('wallace 0.1.0')
        sys.exit(0)
        
    if sys.argv[1] == 'parse':
        if len(sys.argv) == 2 or sys.argv[2] in ['-h', '--help']:
            show_parse_help()
            sys.exit(0)
        if len(sys.argv) != 3:
            print("wallace: error: parse command requires exactly one file argument")
            sys.exit(1)
        process_file(sys.argv[2])
    else:
        print(f"wallace: error: unknown command '{sys.argv[1]}'")
        sys.exit(1)

### SECTION: entry @0.1.0
if __name__ == '__main__':
    main()
