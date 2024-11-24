#!/usr/bin/env python3

#### META: Title: Wallace WAL Format Validator
#### META: Version: 0.1.1
#### META: Author: Claude + Human
#### META: PATH: src/wallace/wal_validator.py

#### SYNOPSIS: WAL file format validator for Wallace.
#### SYNOPSIS: Implements strict validation per spec 0.1.1.
#### SYNOPSIS: Handles both structural and semantic validation.

#### CONTENTS:

from typing import Dict, List, Any, Optional
from .core import WallaceError

def is_valid_wal(wal_json: Dict[str, Any]) -> bool:
    """
    Validate WAL file JSON structure against spec 0.1.1.
    Returns True if valid, False otherwise.
    """
    try:
        # Validate basic structure
        if not isinstance(wal_json, dict):
            return False
            
        required_keys = {"wallace_version", "file_type", "structure"}
        if not all(key in wal_json for key in required_keys):
            return False
            
        if wal_json["file_type"] != "wal":
            return False
            
        # Validate structure requirements
        structure = wal_json["structure"]
        if not isinstance(structure, dict):
            return False
            
        # Validate shebang
        if "shebang" not in structure:
            return False
        if not structure["shebang"].startswith("#!/usr/bin/env wallace"):
            return False
            
        # Validate header block
        if "header_block" not in structure:
            return False
            
        header = structure["header_block"]
        if not isinstance(header, dict):
            return False
            
        # Validate required header components
        required_header = {"meta_block", "synopsis_block", "contents_tag"}
        if not all(key in header for key in required_header):
            return False
            
        # Validate META block
        meta_block = header["meta_block"]
        if not isinstance(meta_block, list):
            return False
            
        required_meta = {"Title", "Version", "Author", "PATH"}
        found_meta = {tag["key"] for tag in meta_block if tag.get("tag") == "META"}
        if not required_meta.issubset(found_meta):
            return False
            
        # Validate SYNOPSIS block
        synopsis_block = header["synopsis_block"]
        if not isinstance(synopsis_block, list) or not synopsis_block:
            return False
            
        # All basic validations passed
        return True
        
    except (KeyError, AttributeError, TypeError):
        return False

def validate_sections(contents_block: List[Dict[str, Any]]) -> bool:
    """
    Validate section structure in contents block.
    Returns True if valid, False otherwise.
    """
    section_stack = []
    
    for item in contents_block:
        if not isinstance(item, dict):
            return False
            
        if item.get("type") == "section":
            name = item.get("name")
            end = item.get("end")
            
            if not name or not end:
                return False
                
            if name != end:
                return False
                
            if not validate_section_content(item.get("content", [])):
                return False
                
            section_stack.append(name)
            
        elif item.get("type") == "end_section":
            if not section_stack:
                return False
            if item.get("name") != section_stack.pop():
                return False
                
    return len(section_stack) == 0

def validate_section_content(content: List[Dict[str, Any]]) -> bool:
    """
    Validate content within a section.
    Returns True if valid, False otherwise.
    """
    valid_tags = {
        "TODO", "DONE", "FIXME", "IDEA", "REVIEW",
        "NOTE", "TRIAGE", "METRICS", "TAGS",
        "FUNCTION", "LINK"
    }
    
    for item in content:
        if not isinstance(item, dict):
            return False
            
        tag = item.get("tag")
        if not tag or tag not in valid_tags:
            return False
            
        if tag == "METRICS":
            if not validate_metrics(item.get("values", [])):
                return False
                
    return True

def validate_metrics(metrics: List[Dict[str, Any]]) -> bool:
    """
    Validate METRICS tag values.
    Returns True if valid, False otherwise.
    """
    valid_units = {"%", "mins", "hrs", "days"}
    
    for metric in metrics:
        if not isinstance(metric, dict):
            return False
            
        if "value" not in metric or "unit" not in metric:
            return False
            
        value = metric["value"]
        unit = metric["unit"]
        
        if not isinstance(value, (int, float)):
            return False
            
        if not isinstance(unit, str) or (unit not in valid_units and
            not unit.isalpha()):
            return False
            
    return True
