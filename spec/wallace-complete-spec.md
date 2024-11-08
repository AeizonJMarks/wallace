# Wallace Language Specification
Version 0.0.2-alpha
November 2024

## Abstract

Wallace is a meta-programming language implemented through source code comments, designed to facilitate human-AI collaboration in software development and project management. It provides a structured approach to code documentation, project management, and system understanding that serves both human comprehension and AI analysis capabilities.

## 1. Introduction

### 1.1 Purpose
Wallace creates a unified layer for code documentation, project management, and human-AI collaboration through structured comments. It serves as both a documentation standard and a project management tool embedded directly in the codebase.

### 1.2 Design Philosophy
- Support human cognitive patterns while not being constrained by them
- Maintain simplicity while allowing full expressiveness
- Support both human readability and AI processing
- Integrate seamlessly with existing tools and workflows
- Preserve project knowledge and decision history
- Enable effective human-AI collaboration

## 2. Core Concepts

### 2.1 Directory Structure
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
└── src/                      # Project source files
```

### 2.2 Comment Hierarchy
```
Level | Marker | Purpose
------|--------|------------------
1     | ;;;;   | File/module level
2     | ;;;    | Section level
3     | ;;     | Block level
4     | ;      | Line level
```

### 2.3 Core Instructions
1. META: File metadata and properties
2. VERSION: Version control information
3. SECTION: Code organization (with END tag)
4. TODO: Planned work items
5. FIXME: Issues requiring attention
6. LINK: Cross-references and dependencies
7. SYNOPSIS: AI-generated system analysis
8. RETRO: Legacy comment management
9. FUNC: Function documentation
10. IDEA: Future possibilities
11. REVIEW: Discussion points
12. TAG: Extension mechanism (reserved)

## 3. Instruction Specifications

### 3.1 META
Purpose: Define file-level metadata
Syntax: `;;;; META: <key>: <value>`
Location: File header only

Required Keys:
- Title
- Version
- Author

Optional Keys:
- Category
- Status
- Dependencies
- Language
- API-Version
- MIN-Version

Example:
```
;;;; META: Title: Core System Module
;;;; META: Version: 0.2.0
;;;; META: Author: Development Team
;;;; META: Category: System
;;;; META: Status: Beta
;;;; META: Language: Python
;;;; META: API-Version: 2
;;;; META: MIN-Version: 1.5.0
```

### 3.2 VERSION
Purpose: Track version information and changes
Syntax: `;;;; VERSION: <major>.<minor>.<patch> [@<status>] [#<hash>]`
Followed by: `;;;; VERSION-CHANGES: <description>`

Status Values:
- @alpha: Early development
- @beta: Feature complete, testing
- @rc: Release candidate
- @stable: Production ready

Example:
```
;;;; VERSION: 0.2.0 @beta #abc123
;;;; VERSION-CHANGES: Added error handling system
```

### 3.3 SECTION
Purpose: Organize code into logical blocks
Syntax: 
```
;;; SECTION: <name> [@<version>]
... content ...
;;; END: SECTION
```

Nesting Allowed:
```
;;; SECTION: outer
;;; SECTION: inner
... content ...
;;; END: inner
;;; END: outer
```

### 3.4 TODO
Purpose: Track planned work items
Syntax: `;; TODO: <description> [@<tag>=<value>]`

Common Tags:
- @priority=1-5
- @assignee=<name>
- @due=YYYY-MM-DD
- @cost=$<amount>
- @effort=<time><unit>
- @blocked-by=<id>
- @depends=<id>

Example:
```
;; TODO: Add input validation @priority=1 @due=2024-12-01 @effort=3days
;; TODO: Update dependencies @cost=$500 @assignee=john
```

### 3.5 FIXME
Purpose: Identify issues requiring attention
Syntax: `;; FIXME: <description> [@<tag>=<value>]`
Tags: Same as TODO

Example:
```
;; FIXME: Memory leak in connection pool @priority=1
;; FIXME: Race condition in auth @effort=2days @cost=$1000
```

### 3.6 LINK
Purpose: Create cross-references and dependencies
Syntax: `;; LINK: <path>[:<line>][#<section>] [@<tag>]`

Formats:
- File references: `file.ext`
- Line references: `file.ext:42`
- Section references: `file.ext#section-name`
- URIs: `https://...`
- Git references: `git:commit-hash`
- Issue references: `issue:number`

Attributes:
- @version=<version>
- @type=<dependency|reference|documentation>
- @status=<active|deprecated|planned>

Example:
```
;; LINK: database.py#connection-pool @type=dependency
;; LINK: docs/architecture.md:156 @version=2.0.0
;; LINK: git:abc123#security-fix
;; LINK: issue:472 @status=active
```

### 3.7 SYNOPSIS
Purpose: AI-generated system analysis
Syntax: `;;;; SYNOPSIS: <analysis>`

Requirements:
- Must be AI-generated
- Must consider full system context
- Must identify key relationships
- Must track critical paths
- Must highlight implications
- Must update with system changes

Example:
```
;;;; SYNOPSIS: Core authentication module controlling system access.
;;;; Critical dependency for user-management.el and session.el.
;;;; Current bottleneck during high-load periods (see perf-metrics.el).
;;;; Recent security audit (security-review.md) suggests
;;;; updating hashing algorithm. Dependencies on deprecated
;;;; crypto library need addressing within next two release cycles.
;;;; Primary scalability constraint for system growth.
```

### 3.8 RETRO
Purpose: Manage legacy comments
Syntax: `;; RETRO: [<YYYY-MM-DD>] <content>`

Example:
```
;; RETRO: [2023-05-15] Original implementation notes:
;; Complex but necessary workaround for API limitation
;; @author=previous-developer
;; @context=legacy-system-constraints
```

### 3.9 FUNC
Purpose: Document function behavior and effects
Syntax:
```
;; FUNC: name(params) -> return_type
;; PURE: yes/no
;; EFFECTS: [list of side effects]
;; COMPLEXITY: O(n)
;; THROWS: [list of exceptions]
```

Example:
```
;; FUNC: calculate_total(items: List[Item], tax_rate: float) -> float
;; PURE: yes
;; EFFECTS: none
;; COMPLEXITY: O(n)
;; THROWS: ValueError on negative tax_rate

;; FUNC: save_user_preferences(user: User, prefs: Dict) -> bool
;; PURE: no
;; EFFECTS: filesystem write, database update
;; COMPLEXITY: O(1)
;; THROWS: IOError, DatabaseError
```

### 3.10 IDEA
Purpose: Document potential improvements or future features
Syntax: `;; IDEA: <description> [@<tag>=<value>]`

Tags:
- @impact=<high|medium|low>
- @difficulty=<high|medium|low>
- @category=<feature|optimization|refactor>

Example:
```
;; IDEA: Add caching layer for frequent queries @impact=high
;; IDEA: Implement batch processing @difficulty=medium
```

### 3.11 REVIEW
Purpose: Mark code for review or discussion
Syntax: `;; REVIEW: <description> [@<tag>=<value>]`

Tags:
- @reviewer=<name>
- @due=<YYYY-MM-DD>
- @type=<security|performance|design|logic>

Example:
```
;; REVIEW: Authentication flow @type=security @reviewer=security-team
;; REVIEW: Query optimization @type=performance @due=2024-12-01
```

### 3.12 Numeric Format
Purpose: Standardize number representation
Format: `<currency_symbol><digits>[.<digits>]<unit>`

Units:
- Time: mins, hrs, days, weeks, months, years
- Currency: $, £, €, ¥
- Percentage: %
- Memory: KB, MB, GB
- Performance: ms, s

Examples:
```
;; TODO: Optimize query @effort=3hrs
;; FIXME: Memory leak @impact=500MB
;; TODO: Update service @cost=$1500
;; REVIEW: Load test @target=500ms
```

## 4. Version Control Integration

### 4.1 Git Integration
```json
{
  "wallace_versions": {
    "0.2.0": {
      "git_hash": "abc123",
      "sections": {
        "core/init": "0.2.0",
        "core/auth": "0.1.0"
      },
      "synopsis_updates": [
        {
          "file": "core.el",
          "hash": "def456",
          "timestamp": "2024-11-07T10:30:00Z"
        }
      ]
    }
  }
}
```

## 5. Implementation Requirements

### 5.1 Parser Requirements
- Full UTF-8 support (future)
- ASCII support (current)
- Robust error handling
- Clear error messages
- Version validation
- Link verification

### 5.2 Editor Integration
- Syntax highlighting
- Tag completion
- Version tracking
- Link resolution
- Synopsis updates

## 6. Future Considerations

### 6.1 Extended Character Support
- Full Unicode support
- International language support
- Custom comment markers
- Rich text formatting

### 6.2 Tool Integration
- CI/CD pipeline integration
- Project management tools
- Documentation generators
- Metrics dashboards

## Appendix A: Language Support

```
Language   | Single Line | Block Start | Block End
-----------|-------------|-------------|----------
C/C++      | //         | /*          | */
Python     | #          | '''         | '''
JavaScript | //         | /*          | */
Java       | //         | /*          | */
Ruby       | #          | =begin      | =end
Go         | //         | /*          | */
Rust       | //         | /*          | */
PHP        | //         | /*          | */
Lisp       | ;          | #|          | |#
HTML/XML   | <!--       | <!--        | -->
```

## Appendix B: Complete Example

```elisp
;;;; META: Title: Authentication System
;;;; META: Version: 0.2.0
;;;; META: Author: Security Team
;;;; META: Category: Security
;;;; META: API-Version: 2

;;;; VERSION: 0.2.0 @beta #def456
;;;; VERSION-CHANGES: Added two-factor authentication

;;;; SYNOPSIS: Primary authentication module handling user access.
;;;; Critical path for user-session.el and admin-panel.el.
;;;; Current implementation uses deprecated hashing algorithm
;;;; (see security-audit.md). Two-factor auth addition
;;;; requires database schema update (see db-migrations/).
;;;; Performance bottleneck at 10k+ concurrent users.

;;; SECTION: initialization @0.2.0
;; FUNC: init_auth() -> bool
;; PURE: no
;; EFFECTS: database connection, logger initialization
;; COMPLEXITY: O(1)

;; TODO: Add startup validation @priority=1 @effort=2days
;; LINK: config.el#system-init @type=dependency

;; RETRO: [2023-01-15] Original implementation used MD5
;; FIXME: Update to Argon2 hashing @priority=1 @cost=$2000

;; IDEA: Add biometric authentication @impact=high
;; REVIEW: Security flow @type=security @due=2024-12-01

(defun init-auth ()
  ...)
;;; END: SECTION

;;; SECTION: user-authentication @0.2.0
;; FUNC: authenticate_user(credentials: Dict) -> bool
;; PURE: no
;; EFFECTS: database read, session creation
;; COMPLEXITY: O(log n)
;; THROWS: AuthError, DatabaseError

(defun authenticate-user (credentials)
  ...)
;;; END: SECTION
```

Copyright © 2024 Wallace Language Specification
