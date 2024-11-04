# Wallace: A Beginner's Guide
*A Human-AI Collaborative Programming Language*

## Introduction

Welcome to Wallace! If you're reading this guide, you're about to discover a new way of thinking about code documentation and management. Wallace isn't your typical programming language - it's a language that lives in the comments of your code, designed specifically for humans and AI to work together effectively.

## What Makes Wallace Different?

Think of Wallace as a conversation layer that sits above your regular programming language. Just like you might use comments to explain code to other developers, Wallace uses comments to create a structured dialogue between humans and AI.

## Getting Started

### The Basics
Wallace uses your language's comment syntax. In this guide, we'll use Lisp-style comments (;) as examples, but the principles apply to any language with comment support.

### Core Concepts

#### 1. File Headers
Every Wallace file starts with metadata:
```elisp
;;;; META: Title: My First Wallace File
;;;; META: Version: 1.0.0
;;;; VERSION: 1.0.0 @stable
;;;; VERSION-CHANGES: Initial version
```

#### 2. Sections
Organize your code into clear sections:
```elisp
;;; SECTION_START: user-interface
;; This section handles user interaction
(defun greet-user ()
  (message "Hello!"))
;;; SECTION_END: user-interface
```

#### 3. Tasks and Issues
Mark things that need attention:
```elisp
;; TODO: Add input validation @priority=1
;; FIXME: Function crashes with empty input
```

#### 4. Links and References
Connect related pieces of code:
```elisp
;; LINK: utils.el#error-handling
;; LINK: docs/api.md
```

### Best Practices

1. **Keep It Simple**
   - Use clear, descriptive section names
   - Keep tasks focused and specific
   - Don't overuse tags

2. **Version Properly**
   ```elisp
   ;;;; VERSION: 1.1.0 @beta
   ;;;; VERSION-CHANGES: Added new user interface
   ```

3. **Link Wisely**
   - Use relative paths when possible
   - Link to specific sections when relevant
   - Include line numbers for precise references

## Common Patterns

### 1. Feature Development
```elisp
;;;; META: Title: User Authentication
;;;; VERSION: 1.0.0 @beta

;;; SECTION_START: authentication @1.0.0
;; TODO: Add password hashing @priority=1
;; LINK: security.el#hashing
(defun authenticate-user (username password)
  ...)
;;; SECTION_END: authentication
```

### 2. Bug Fixing
```elisp
;;; SECTION_START: data-validation
;; FIXME: Fails with unicode input
;; LINK: test/validation-test.el:42
(defun validate-input (text)
  ...)
;;; SECTION_END: data-validation
```

### 3. Feature Planning
```elisp
;;; SECTION_START: future-features
;; IDEA: Add biometric authentication
;; LINK: docs/biometric-spec.md
;;; SECTION_END: future-features
```

## Working with AI

Wallace is designed for AI collaboration. Here's how to make the most of it:

1. **Be Explicit**
   ```elisp
   ;; TODO: Optimize database query @priority=1
   ;; Current query takes 5s for 1000 records
   ```

2. **Use Links**
   ```elisp
   ;; LINK: slow-query.el:15 @performance
   ;; LINK: docs/performance-guide.md#queries
   ```

3. **Track Versions**
   ```elisp
   ;;;; VERSION: 1.2.0 @rc #abc123
   ;;;; VERSION-CHANGES: Improved query performance
   ```

## Common Questions

### Q: How many sections should I have?
A: Keep it manageable - typically 3-7 main sections per file. Remember Miller's Law about human cognitive limits.

### Q: When should I increment versions?
A: Follow semantic versioning:
- Major (1.0.0): Breaking changes
- Minor (0.1.0): New features
- Patch (0.0.1): Bug fixes

### Q: How detailed should my comments be?
A: Include enough context for both humans and AI to understand the intent and any important constraints or considerations.

## Tips and Tricks

1. **Use Meaningful Section Names**
   ```elisp
   ;;; SECTION_START: error-handling    ; Good
   ;;; SECTION_START: stuff            ; Bad
   ```

2. **Keep Related Things Together**
   ```elisp
   ;; TODO: Add user validation
   ;; LINK: validation.el
   ;; REVIEW: Security implications
   ```

3. **Version Your Sections**
   ```elisp
   ;;; SECTION_START: authentication @1.1.0
   ;; Added two-factor support
   ```

## Next Steps

1. Start small - add Wallace headers to your existing files
2. Organize your code into logical sections
3. Use TODO and FIXME to track work items
4. Add links between related code
5. Keep your versions updated

## Example Complete File

```elisp
;;;; META: Title: User Management System
;;;; META: Author: Your Name
;;;; META: Updated: 2024-11-03

;;;; VERSION: 1.1.0 @beta #def456
;;;; VERSION-CHANGES: Added password reset functionality

;;; SECTION_START: initialization @1.0.0
;; LINK: config.el#system-init
(defun initialize-user-system ()
  (setup-database)
  (load-user-preferences))
;;; SECTION_END: initialization

;;; SECTION_START: authentication @1.1.0
;; TODO: Add two-factor authentication @priority=2
;; LINK: security.el#auth-methods
(defun authenticate-user (username password)
  ...)
;;; SECTION_END: authentication

;;; SECTION_START: password-reset @1.1.0
;; REVIEW: Consider rate limiting
;; LINK: docs/security-guidelines.md#rate-limits
(defun reset-password (user-id)
  ...)
;;; SECTION_END: password-reset
```

Remember: Wallace is about communication first. Write your comments thinking about both human readers and AI collaborators, and you'll be using Wallace effectively!

## Need Help?

- Review the official specification
- Check example files
- Start with small, focused changes
- Build up to more complex usage

Happy coding with Wallace!
