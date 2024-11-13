# Wallace Language Specification
Version 0.0.8-alpha
November 2024

## Abstract

Wallace is a meta-programming language implemented through source code comments, designed to facilitate human-AI collaboration in software development. This specification defines the complete syntax, semantics, and implementation requirements for Wallace, including both embedded and standalone (.wal) formats.

## 1. Introduction

[Previous introduction content remains the same...]

## 2. Fundamental Concepts

### 2.1 Basic Rules
[Previous rules remain the same...]

### 2.2 Comment Markers
```
Language   | Single Line | Block Start | Block End
-----------|-------------|-------------|----------
Python     | #          | '''         | '''
.wal       | #          | '''         | '''
```

### 2.3 Comment Hierarchy
```
Level | Marker | Purpose
------|--------|------------------
1     | ####   | File/module level
2     | ###    | Section level
3     | ##     | Block level
4     | #      | Line level
```

### 2.4 Core Instructions
1. META: File metadata and properties
2. TAGS: Declaration of extended tag usage
3. VERSION: Version control information
4. SECTION: Code organization
5. TODO: Planned work items
6. FIXME: Issues requiring attention
7. LINK: Cross-references and dependencies
8. SYNOPSIS: AI-generated system analysis
9. RETRO: Legacy comment management
10. FUNCTION: Function documentation
11. IDEA: Future possibilities
12. REVIEW: Discussion points
13. TAG: Extension mechanism (reserved)
14. END: Explicit block termination
15. DONE: Task completion marker

## 3. Task Management System

### 3.1 TODO and DONE Relationship
Tasks flow from TODO to DONE with timestamp tracking:

```python
# TODO: Implement rate limiting @priority=1 @created=2024-11-08T14:30:00Z

# Later, when completed:
# DONE: Implement rate limiting @completed=2024-11-10T16:45:00Z @commit=abc123
```

### 3.2 Task Resolution Rules
1. DONE tags must match original TODO text
2. Timestamp must be in ISO 8601 format
3. Git commit hash must be included
4. Original TODO attributes preserved for reference
5. Both entries maintained in history

### 3.3 Task Status Tracking
The .wallace directory maintains task history:

```json
{
  "tasks": {
    "rate-limiting-implementation": {
      "type": "TODO",
      "description": "Implement rate limiting",
      "created": "2024-11-08T14:30:00Z",
      "priority": 1,
      "completed": "2024-11-10T16:45:00Z",
      "commit": "abc123",
      "file": "auth.py",
      "line": 42
    }
  }
}
```

[Rest of the specification continues with updated Python syntax...]

## Examples

### Example 1: Python Source File
```python
#### META: Title: Authentication System
#### META: Version: 1.0.0
#### META: Author: Security Team
#### TAGS: VERSION-CHANGES EFFECTS

#### VERSION: 1.0.0 @beta #abc123
#### VERSION-CHANGES: Initial authentication system

#### SYNOPSIS: Core authentication module for system.
#### SYNOPSIS: Handles OAuth2 with rate limiting.
#### END: SYNOPSIS

### SECTION: auth_core @1.0.0
## FUNCTION: authenticate(user: str, pwd: str) -> bool
## PURE: no
## EFFECTS: database read, session write

def authenticate(user: str, pwd: str) -> bool:
    # Standard code comment
    pass

# TODO: Add rate limiting @priority=1 @created=2024-11-08T14:30:00Z
# LINK: docs/rate-limits.md
### END: SECTION
```

### Example 2: .wal File
```wallace
#### META: Title: Authentication System
#### META: Version: 1.0.0
#### META: Author: Security Team
#### TAGS: VERSION-CHANGES EFFECTS

#### VERSION: 1.0.0 @beta #abc123
#### VERSION-CHANGES: Initial implementation

#### SYNOPSIS: Core authentication module.
#### SYNOPSIS: Needs rate limiting implementation.
#### END: SYNOPSIS

### SECTION: auth_core @1.0.0
## FUNCTION: authenticate(user: str, pwd: str) -> bool
## PURE: no
## EFFECTS: database read, session write
## LINK: auth.py:42 @type=implementation

# TODO: Add rate limiting @priority=1 @created=2024-11-08T14:30:00Z
# DONE: Add basic auth @completed=2024-11-07T15:20:00Z @commit=def456
### END: SECTION
```

[Rest of specification continues with grammar updates...]

Copyright © 2024 Wallace Language Specification