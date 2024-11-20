#!/usr/bin/env python3

#### META: Title: Wallace Command Line Tool
#### META: Version: 0.1.0
#### META: Author: Claude + Human
#### META: Path: ~/wallace/wallace.py
#### TAGS: MANUAL COMMANDS

#### VERSION: 0.1.0 @alpha #abc123

#### SYNOPSIS: Core Wallace command line tool.
#### SYNOPSIS: Implements distinct handling for .txt files as prompt/thought flow.
#### SYNOPSIS: Provides unified interface for Wallace operations.
#### SYNOPSIS: Added comprehensive file type handling with proper comment syntax.
#### SYNOPSIS: Added Unix-style verbosity control with proper error reporting.
#### SYNOPSIS: Fixed language-specific prefix validation.

### SECTION: imports @0.1.0
import sys
import argparse
import re
from pathlib import Path

### SECTION: file_types @0.1.0
# Mapping of file extensions to comment syntax
FILE_TYPES = {
   # Lisp family
   '.el': {
       'single': ';',        # Single line comment
       'prefix': ';;;; ',    # Wallace tag prefix (4 semicolons + space)
       'continue': ';;;; '   # Continuation prefix
   },
   # Python family
   '.py': {
       'single': '#',
       'prefix': '#### ',
       'continue': '#### '
   },
   # Shell scripts
   '.sh': {
       'single': '#',
       'prefix': '#### ',
       'continue': '#### '
   },
   # C family
   '.c': {
       'single': '//',
       'prefix': '//// ',
       'continue': '//// '
   },
   '.cpp': {
       'single': '//',
       'prefix': '//// ',
       'continue': '//// '
   },
   '.h': {
       'single': '//',
       'prefix': '//// ',
       'continue': '//// '
   },
   # Web languages
   '.js': {
       'single': '//',
       'prefix': '//// ',
       'continue': '//// '
   },
   '.css': {
       'single': '/*',
       'prefix': '/***** ',
       'continue': '***** '
   },
   # Special cases
   '.txt': {
       'single': '',         # No comment syntax
       'prefix': '',         # Tags can appear anywhere
       'continue': ''        # No continuation needed
   },
   '.md': {
       'single': '',         # Markdown is like txt
       'prefix': '',
       'continue': ''
   }
}

### SECTION: core_functions @0.1.0

### FUNCTION: get_file_syntax(file_path: str) -> dict
### PURE: yes
### EFFECTS: none
def get_file_syntax(file_path: str) -> dict:
   """Get comment syntax for a file type."""
   ext = Path(file_path).suffix.lower()
   if ext not in FILE_TYPES:
       raise ValueError(f"Unsupported file type: {ext}")
   return FILE_TYPES[ext]

### FUNCTION: parse_txt_content(content: str) -> list
### PURE: yes
### EFFECTS: none
def parse_txt_content(content: str) -> list:
   """Parse .txt content for Wallace tags with thought-flow rules."""
   matches = []
   pattern = r'(?:^|\s)([A-Z]+):\s(.+?)(?:\.|$)'
   
   for i, line in enumerate(content.splitlines(), 1):
       for match in re.finditer(pattern, line):
           tag_name, content = match.groups()
           
           # Validate tag name is only uppercase letters
           if not re.match(r'^[A-Z]+$', tag_name):
               continue
               
           matches.append({
               'line': i,
               'position': match.start(),
               'tag': tag_name,
               'content': content.strip(),
               'raw': match.group()
           })
   
   return matches

### FUNCTION: parse_source_content(content: str, syntax: dict) -> list
### PURE: yes
### EFFECTS: none
def parse_source_content(content: str, syntax: dict) -> list:
   """Parse source file content using appropriate syntax."""
   matches = []
   current_tag = None
   tag_content = []
   
   # Create pattern using file-specific prefix
   pattern = rf'^\s*{re.escape(syntax["prefix"])}([A-Z]+):\s(.+)$'
   
   for i, line in enumerate(content.splitlines(), 1):
       match = re.match(pattern, line)
       
       if match:
           if current_tag:
               matches.append({
                   'line': current_tag['line'],
                   'position': current_tag['position'],
                   'tag': current_tag['tag'],
                   'content': '\n'.join(tag_content),
                   'raw': current_tag['raw']
               })
           
           tag_name, content = match.groups()
           current_tag = {
               'line': i,
               'position': match.start(),
               'tag': tag_name,
               'raw': match.group()
           }
           tag_content = [content]
       elif current_tag:
           # Check if this is a continuation line
           continue_pattern = rf'^\s*{re.escape(syntax["continue"])}(.+)$'
           continue_match = re.match(continue_pattern, line)
           if continue_match:
               tag_content.append(continue_match.group(1))
           else:
               # Not a continuation, end current tag
               matches.append({
                   'line': current_tag['line'],
                   'position': current_tag['position'],
                   'tag': current_tag['tag'],
                   'content': '\n'.join(tag_content),
                   'raw': current_tag['raw']
               })
               current_tag = None
   
   if current_tag:
       matches.append({
           'line': current_tag['line'],
           'position': current_tag['position'],
           'tag': current_tag['tag'],
           'content': '\n'.join(tag_content),
           'raw': current_tag['raw']
       })
   
   return matches

### FUNCTION: process_file(file_path: str, verbose: bool) -> None
### PURE: no
### EFFECTS: filesystem read, stdout write
def process_file(file_path: str, verbose: bool) -> None:
    """Process a file and display found tags if verbose."""
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"wallace: error: file '{file_path}' does not exist", file=sys.stderr)
            sys.exit(1)
        
        # Get syntax for file type
        try:
            syntax = get_file_syntax(str(path))
        except ValueError as e:
            print(f"wallace: error: {str(e)}", file=sys.stderr)
            sys.exit(1)
        
        with open(file_path, 'r') as f:
            content = f.read()

        # Track errors
        errors = []
        
        # Define file-specific patterns
        if path.suffix in ['.txt', '.md']:
            # For .txt files, tags can appear anywhere
            valid_tag_pattern = r'(?:^|\s)([A-Z]+):\s'
        else:
            # For source files, we have two valid patterns:
            # 1. Standard tags with full prefix (e.g., #### META:)
            # 2. Section tags with three comment chars (e.g., ### SECTION:)
            standard_prefix = re.escape(syntax["prefix"])  # e.g., #### for Python
            section_prefix = re.escape(syntax["single"] * 3 + " ")  # e.g., ### for Python
            
            valid_tag_pattern = f'(?:{standard_prefix}[A-Z]+:\\s|{section_prefix}(?:SECTION|END):\\s)'
            
        # Parse and validate content
        for line_number, line in enumerate(content.splitlines(), 1):
            # Skip empty lines or regular comments
            if not line.strip() or line.strip().startswith(syntax["single"]):
                continue
                
            # Check if line contains a tag-like pattern
            if re.search(r'[A-Z]+:', line):
                # For source files, validate prefix
                if path.suffix not in ['.txt', '.md']:
                    if not re.match(valid_tag_pattern, line):
                        errors.append(f"Line {line_number}: Invalid tag prefix")
                        continue
                
                # Check common errors for any tag
                if re.search(r'[A-Z]+:[^\s]', line):  # Missing space after colon
                    errors.append(f"Line {line_number}: Missing space after colon")
                elif re.search(r'[a-z]+:', line):  # Lowercase tag
                    errors.append(f"Line {line_number}: Tag must be uppercase")
        
        # Use appropriate parser based on file type
        if path.suffix in ['.txt', '.md']:
            matches = parse_txt_content(content)
        else:
            matches = parse_source_content(content, syntax)
            
        # In non-verbose mode, report errors or exit silently
        if not verbose:
            if errors:
                for error in errors:
                    print(f"wallace: error: {error}", file=sys.stderr)
                sys.exit(1)
            if not matches:
                print(f"wallace: error: no valid Wallace tags found in {file_path}", file=sys.stderr)
                sys.exit(1)
            sys.exit(0)
            
        # In verbose mode, display full results and any errors
        if errors:
            print("\nErrors found:")
            for error in errors:
                print(f"  {error}")
            print()
        display_results(matches, file_path)
        
        # Exit with error if any errors found, even in verbose mode
        if errors:
            sys.exit(1)
        
    except Exception as e:
        print(f"wallace: error: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
### FUNCTION: display_results(matches: list, source: str) -> None
### PURE: no
### EFFECTS: stdout write
def display_results(matches: list, source: str) -> None:
   """Display parsing results."""
   print(f"\nAnalyzing {source}:")
   if not matches:
       print("No Wallace tags found.")
       return
   
   print(f"\nFound {len(matches)} tags:\n")
   for match in matches:
       print(f"Line {match['line']}, Pos {match['position']}:")
       print(f"  Tag: {match['tag']}")
       print(f"  Content: {match['content']}")
       print()

### FUNCTION: main() -> None
### PURE: no
### EFFECTS: argv read, filesystem read, stdout write
def main() -> None:
   """Main entry point for Wallace command line tool."""
   parser = argparse.ArgumentParser(description='Wallace development tool')
   parser.add_argument('-v', '--verbose', action='store_true',
                      help='enable verbose output')
   parser.add_argument('--version', action='store_true',
                      help='show program version')
   
   subparsers = parser.add_subparsers(dest='command')
   
   # Parse command
   parse_cmd = subparsers.add_parser('parse', 
                                    help='validate Wallace tag syntax',
                                    description="""Validate Wallace tag syntax in files.
                                    
Without -v, silently succeed if valid tags found.""")
   parse_cmd.add_argument('file', help='file to parse')
   
   args = parser.parse_args()
   
   if args.version:
       print('wallace 0.1.0')
       sys.exit(0)
       
   if args.command == 'parse':
       process_file(args.file, args.verbose)
   elif args.command is None:
       parser.print_help()
       sys.exit(0)
   else:
       print(f"wallace: error: unknown command '{args.command}'", file=sys.stderr)
       sys.exit(1)

### SECTION: entry @0.1.0
if __name__ == '__main__':
   main()
