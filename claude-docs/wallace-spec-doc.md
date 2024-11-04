# Wallace Language Specification
Version 1.0.0-rc1  
November 2024

## Abstract

Wallace is a meta-programming language implemented through source code comments, designed to facilitate human-AI collaboration in software development. This specification defines the syntax, semantics, and implementation requirements for Wallace.

## 1. Introduction

### 1.1 Purpose
Wallace provides a structured approach to code documentation and management that serves both human cognitive constraints and AI processing capabilities. It operates as a layer above traditional programming languages, using their comment systems as its implementation medium.

### 1.2 Scope
This specification defines:
- Language syntax and semantics
- Core instruction set
- Version control integration
- Extension mechanisms
- Implementation requirements

### 1.3 Conformance
A Wallace implementation must support all core instructions and syntax rules defined in this specification. Extensions are optional but must follow the extension rules when implemented.

## 2. Language Overview

### 2.1 Design Principles
1. Human-Centric: Respects cognitive limits (Miller's Law)
2. Language-Agnostic: Functions across programming languages
3. Unambiguous: Clear, consistent syntax
4. Extensible: Allows controlled growth
5. Version-Aware: Integrates with version control

### 2.2 Core Features
- Hierarchical structure
- Semantic versioning
- Cross-referencing system
- Task management
- Documentation integration

## 3. Syntax and Semantics

### 3.1 Character Set
Wallace uses UTF-8 encoding. Comments must use ASCII for instruction keywords.

### 3.2 Comment Markers
```
Language   | Single Line | Block Start | Block End
-----------|-------------|-------------|----------
Lisp       | ;          | N/A         | N/A
Python     | #          | '''         | '''
JavaScript | //         | /*          | */
HTML       | <!--       | <!--        | -->
SQL        | --         | /*          | */
```

### 3.3 Hierarchy
```
Level | Lisp  | Purpose
------|-------|------------------
1     | ;;;; | File/Module level
2     | ;;;  | Section level
3     | ;;   | Block level
4     | ;    | Line level
```

### 3.4 Core Instructions
1. META: File metadata
2. VERSION: Version control information
3. SECTION: Code organization
4. TODO: Planned work
5. FIXME: Issues
6. LINK: Cross-references
7. IDEA: Future possibilities
8. REVIEW: Discussion items

### 3.5 Instruction Syntax

#### META
```
;;;; META: <key>: <value>
```

#### VERSION
```
;;;; VERSION: <major>.<minor>.<patch> [@<status>] [#<hash>]
;;;; VERSION-CHANGES: <description>
```

#### SECTION
```
;;; SECTION_START: <name> [@<version>]
;;; SECTION_END: <name>
```

#### LINK
```
;; LINK: <path>[:<line>][#<section>] [@<tag>]
```

### 3.6 Tags
```
@priority=<1-5>
@status=<pending|in-progress|completed>
@owner=<name>
@due=<YYYY-MM-DD>
```

## 4. Version Control Integration

### 4.1 Semantic Versioning
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### 4.2 Status Indicators
- alpha: Early development
- beta: Feature complete, testing
- rc: Release candidate
- stable: Production ready

### 4.3 Version Control Rules
1. Each file requires VERSION tag
2. SECTION versions must match file version
3. Breaking changes increment major version
4. API changes documented in VERSION-CHANGES

## 5. Extension Mechanism

### 5.1 Custom Instructions
```
;;;; META: WALLACE-EXTENSION: <instruction>
;;;; META: WALLACE-EXTENSION-DESC: <description>
```

### 5.2 Extension Rules
1. Maximum 3 custom instructions per file
2. Must be declared at file level
3. Names must be uppercase
4. Must follow core instruction syntax

## 6. Implementation Requirements

### 6.1 Parser Requirements
1. Must recognize all core instructions
2. Must validate syntax
3. Must respect hierarchy
4. Must track versions

### 6.2 Editor Integration
1. Syntax highlighting
2. Instruction completion
3. Version validation
4. Link resolution

## 7. Future Considerations

### 7.1 Planned Extensions
1. Project management integration
2. Automated documentation
3. AI-specific instructions
4. Build system integration

### 7.2 Compatibility
Future versions will maintain backward compatibility within major versions.

## Appendix A: Grammar

```ebnf
instruction    ::= meta | version | section | action
meta          ::= ";;;; META:" key ":" value
version       ::= ";;;; VERSION:" semver ["@" status] ["#" hash]
section       ::= section-start content section-end
section-start ::= ";;; SECTION_START:" name ["@" version]
section-end   ::= ";;; SECTION_END:" name
action        ::= ";;" command ":" description ["@" tag]
```

## Appendix B: Examples

Complete file example:
```elisp
;;;; META: Title: Core System
;;;; META: API-VERSION: 2
;;;; META: MIN-VERSION: 1.5.0

;;;; VERSION: 2.1.0 @stable #abc123
;;;; VERSION-CHANGES: Enhanced error handling

;;; SECTION_START: initialization @2.1.0
;; TODO: Add startup logging @priority=1
;; LINK: docs/startup.md#configuration
(defun init-system ()
  ...)
;;; SECTION_END: initialization
```

Copyright © 2024 Wallace Language Specification
