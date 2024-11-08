# Wallace Language Specification
Version 0.0.7-alpha
November 2024

## Abstract

Wallace is a meta-programming language implemented through source code comments, designed to facilitate human-AI collaboration in software development. This specification defines the complete syntax, semantics, and implementation requirements for Wallace, including both embedded and standalone (.wal) formats.

## 1. Introduction

### 1.1 Purpose
Wallace creates a unified layer for code documentation, project management, and human-AI collaboration through structured comments. It serves as both a documentation standard and a project management tool embedded directly in the codebase or in companion files.

### 1.2 Design Philosophy
- Support human cognitive patterns while not being constrained by them
- Maintain simplicity while allowing full expressiveness
- Support both human readability and AI processing
- Integrate seamlessly with existing tools and workflows
- Preserve project knowledge and decision history
- Enable effective human-AI collaboration
- Respect AI autonomy in system analysis
- Maintain clear syntactic boundaries
- Allow flexible deployment (embedded or separate)

## 2. Fundamental Concepts

### 2.1 Basic Rules
1. Each Wallace tag must occupy its own line completely
2. Wallace tags extend from the start to the end of the line
3. Any comment not following Wallace syntax is a standard programmer comment
4. No mixing of Wallace tags with regular comments on the same line
5. Clear separation between Wallace and non-Wallace content
6. Blocks can be terminated explicitly (END tag) or implicitly (blank line)

### 2.2 Directory Structure
```
project-root/
├── .wallace/                  # Wallace metadata directory
│   ├── manifest.json          # Project-wide metadata
│   ├── synopsis/              # AI-generated analysis
│   │   ├── core.el.json      # File-level synopses
│   │   └── system.json       # System-wide insights
│   ├── links/                # Cross-reference mapping
│   │   └── dependencies.json
│   └── versions/             # Version mapping
│       └── version-map.json
├── src/                      # Source files
│   ├── auth.py              # Source with embedded Wallace
│   └── auth.wal             # Optional companion file
└── docs/                     # Documentation
```

### 2.3 Comment Hierarchy
```
Level | Marker | Purpose
------|--------|------------------
1     | ;;;;   | File/module level
2     | ;;;    | Section level
3     | ;;     | Block level
4     | ;      | Line level
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

## 3. File Formats

### 3.1 Embedded Format
Wallace entries directly in source files:
```python
# auth.py
;;;; META: Title: Authentication Module
;;;; META: Version: 1.0.0
;;;; TAGS: VERSION-CHANGES EFFECTS

def authenticate(user):
    # Regular code comment
    pass
```

### 3.2 .wal Format
Pure Wallace companion files:
```wallace
# auth.wal
;;;; META: Title: Authentication Module
;;;; META: Version: 1.0.0
;;;; TAGS: VERSION-CHANGES EFFECTS

;; FUNCTION: authenticate(user: str) -> bool
;; LINK: auth.py:42 @type=implementation
```

### 3.3 Deployment Modes
1. Companion Mode: Separate .wal files
2. Embedded Mode: Wallace in source
3. Hybrid Mode: Combination of both

## 4. Tag Specifications

### 4.1 META and TAGS
Required file-level declarations.

Syntax:
```wallace
;;;; META: <key>: <value>
;;;; TAGS: <space-separated-extension-tags>
```

Required META Keys:
- Title
- Version
- Author

Optional META Keys:
- Category
- Status
- Language
- API-Version
- MIN-Version

Example:
```wallace
;;;; META: Title: Authentication System
;;;; META: Version: 1.0.0
;;;; META: Author: Security Team
;;;; META: Category: Security
;;;; META: Language: Python
;;;; TAGS: VERSION-CHANGES EFFECTS PURE COMPLEXITY THROWS
```

### 4.2 VERSION
Version control information.

Syntax:
```wallace
;;;; VERSION: <major>.<minor>.<patch> [@<status>] [#<hash>]
;;;; VERSION-CHANGES: <description>
```

Status Values:
- @alpha: Early development
- @beta: Feature complete, testing
- @rc: Release candidate
- @stable: Production ready

Example:
```wallace
;;;; VERSION: 1.2.0 @beta #abc123
;;;; VERSION-CHANGES: Added OAuth support
```

### 4.3 SECTION
Code organization blocks.

Syntax:
```wallace
;;; SECTION: <name> [@<version>]
... content ...
;;; END: SECTION
```

Example:
```wallace
;;; SECTION: authentication @1.2.0
;; TODO: Add validation
;;; END: SECTION
```

### 4.4 TODO and FIXME
Task and issue tracking.

Syntax:
```wallace
;; TODO: <description> [@<tag>=<value>]
;; FIXME: <description> [@<tag>=<value>]
```

Common Tags:
- @priority=1-5
- @assignee=<name>
- @due=YYYY-MM-DD
- @cost=<currency><amount>
- @effort=<value><unit>
- @impact=<value><unit>

Time Units:
- mins
- hrs
- days
- weeks
- months
- years

Currency Units:
- $, £, €, ¥
- USD, GBP, EUR, JPY

Memory Units:
- KB, MB, GB, TB

Performance Units:
- ms, s, ns

Examples:
```wallace
;; TODO: Add rate limiting @priority=1 @effort=2days
;; TODO: Update UI @cost=$500 @due=2024-12-25
;; FIXME: Memory leak @impact=500MB
;; FIXME: Slow query @effort=3hrs @priority=1
```

### 4.5 LINK
Cross-reference and dependency tracking.

Syntax:
```wallace
;; LINK: <target>[:<line-number>][#<section>] [@<tag>=<value>]
```

Target Types:
- File references: `file.ext`
- Line references: `file.ext:42`
- Line ranges: `file.ext:42-50`
- Section references: `file.ext#section-name`
- URIs: `https://...`
- Git references: `git:commit-hash`
- Issue references: `issue:number`

Tags:
- @type=<dependency|implementation|reference|documentation>
- @version=<version>
- @status=<active|deprecated|planned>

Examples:
```wallace
;; LINK: auth.py:42 @type=implementation
;; LINK: docs/auth.md#security @version=2.0
;; LINK: git:abc123#security-fix
;; LINK: issue:472 @status=active
```

### 4.6 SYNOPSIS
AI-generated system analysis.

Protocol:
1. Content is 100% AI-generated
2. Represents AI's autonomous analysis
3. Can be discussed but remains under AI control
4. Changes based on AI's judgment
5. Reflects complete system understanding

Syntax:
```wallace
;;;; SYNOPSIS: <analysis-line>
;;;; SYNOPSIS: <analysis-line>
;;;; END: SYNOPSIS
```

Example:
```wallace
;;;; SYNOPSIS: Authentication module handling system access.
;;;; SYNOPSIS: Critical dependency for user-session.el.
;;;; SYNOPSIS: Shows performance degradation above 10k users.
;;;; SYNOPSIS: Requires immediate crypto library upgrade.
;;;; END: SYNOPSIS
```

### 4.7 RETRO
Legacy comment management.

Syntax:
```wallace
;; RETRO: [<YYYY-MM-DD>] <content>
```

Example:
```wallace
;; RETRO: [2023-05-15] Original implementation used MD5
;; RETRO: [2024-01-10] Updated to bcrypt
```

### 4.8 FUNCTION
Function documentation.

Syntax:
```wallace
;; FUNCTION: <name>(<params>) -> <return_type>
;; PURE: <yes|no>
;; EFFECTS: <side-effects>
;; COMPLEXITY: <big-o-notation>
;; THROWS: <exceptions>
```

Example:
```wallace
;; FUNCTION: authenticate(user: str, pass: str) -> bool
;; PURE: no
;; EFFECTS: database read, session creation
;; COMPLEXITY: O(log n)
;; THROWS: AuthError, DatabaseError
```

### 4.9 IDEA and REVIEW
Future possibilities and discussion points.

Syntax:
```wallace
;; IDEA: <description> [@<tag>=<value>]
;; REVIEW: <description> [@<tag>=<value>]
```

Tags:
- @impact=<high|medium|low>
- @difficulty=<high|medium|low>
- @category=<feature|optimization|refactor>
- @reviewer=<name>
- @due=<YYYY-MM-DD>

Examples:
```wallace
;; IDEA: Add biometric auth @impact=high @difficulty=high
;; REVIEW: Security audit needed @reviewer=security-team
```

### 4.10 END
Block termination.

Syntax:
```wallace
<level> END: <tag>
```

Examples:
```wallace
;;; END: SECTION
;;;; END: SYNOPSIS
;; END: REVIEW
```

## 5. Implementation Requirements

### 5.1 Parser Requirements
- Full UTF-8 support (future)
- ASCII support (current)
- Handle both embedded and .wal formats
- Support all numeric formats
- Validate all tags and attributes
- Maintain format conversion capability

### 5.2 Tool Integration
- Editor/IDE support
- Build system integration
- Version control integration
- CI/CD pipeline integration
- Documentation generation
- Metrics dashboard support

### 5.3 Security Considerations
- Sensitive information handling
- Access control support
- Security review integration
- Audit trail maintenance

## Appendix A: Complete Examples

### A.1 Embedded Format Example
```python
# auth.py
;;;; META: Title: Authentication System
;;;; META: Version: 1.0.0
;;;; META: Author: Security Team
;;;; META: Category: Security
;;;; TAGS: VERSION-CHANGES EFFECTS PURE

;;;; VERSION: 1.0.0 @beta #abc123
;;;; VERSION-CHANGES: Initial authentication system

;;;; SYNOPSIS: Core authentication module for system.
;;;; SYNOPSIS: Implements OAuth2 and local authentication.
;;;; SYNOPSIS: Shows potential scaling issues above 10k users.
;;;; END: SYNOPSIS

;;; SECTION: initialization @1.0.0
;; FUNCTION: init_auth() -> bool
;; PURE: no
;; EFFECTS: database connection
;; COMPLEXITY: O(1)

def init_auth():
    # Regular code comment
    pass
;;; END: SECTION
```

### A.2 .wal Format Example
```wallace
# auth.wal
;;;; META: Title: Authentication System
;;;; META: Version: 1.0.0
;;;; META: Author: Security Team
;;;; META: Category: Security
;;;; TAGS: VERSION-CHANGES EFFECTS PURE

;;;; VERSION: 1.0.0 @beta #abc123
;;;; VERSION-CHANGES: Initial authentication system

;;;; SYNOPSIS: Core authentication module for system.
;;;; SYNOPSIS: Implements OAuth2 and local authentication.
;;;; SYNOPSIS: Shows potential scaling issues above 10k users.
;;;; END: SYNOPSIS

;;; SECTION: initialization @1.0.0
;; FUNCTION: init_auth() -> bool
;; PURE: no
;; EFFECTS: database connection
;; COMPLEXITY: O(1)
;; LINK: auth.py:15-28 @type=implementation

;; TODO: Add startup validation @priority=1
;; LINK: auth.py:22 @type=target

;; REVIEW: Security audit needed @due=2024-12-25
;; LINK: auth.py:15-150 @type=scope
;;; END: SECTION
```

## Appendix B: Grammar

```ebnf
wallace-file    ::= meta-block version-block synopsis-block content
meta-block      ::= meta-tag+ tags-tag?
meta-tag        ::= ";;;; META:" key ":" value EOL
tags-tag        ::= ";;;; TAGS:" extension-tag+
version-block   ::= version-tag version-changes-tag
synopsis-block  ::= synopsis-tag+ end-synopsis
content         ::= section | todo | fixme | link | function | idea | review
section         ::= section-start content* section-end
section-start   ::= ";;; SECTION:" name ["@" version] EOL
section-end     ::= ";;; END: SECTION" EOL
todo            ::= ";; TODO:" description [attributes] EOL
fixme           ::= ";; FIXME:" description [attributes] EOL
link            ::= ";; LINK:" target ["@" type] EOL
function        ::= ";; FUNCTION:" signature EOL effects complexity throws
end-tag         ::= level "END:" tag-type EOL
```

Copyright © 2024 Wallace Language Specification
