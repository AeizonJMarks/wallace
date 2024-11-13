# Wallace: A Complete Human's Guide
*Your comprehensive guide to human-AI collaboration through code*

## Welcome to Wallace! 

Have you ever wished you could have a conversation with your code? Or wanted a way to manage projects that stays perfectly in sync with your actual work? That's exactly what Wallace helps you do! This guide will show you how Wallace makes software development more human, more organized, and more collaborative.

## What is Wallace?

Wallace is a powerful yet friendly way of writing comments in your code that turns them from simple notes into a complete project management and collaboration system. Think of it like having a conversation with both your fellow developers and AI assistants, right in the code itself.

Don't worry if you're new to programming - if you can write notes to yourself, you can use Wallace!

## Getting Started

### The Basics: Writing Wallace Comments

Wallace uses a simple hierarchy based on how many comment markers you use:
```
;;;; Four for important file information
;;; Three for major sections
;; Two for regular notes
; One for quick notes
```

Here's your first Wallace file:

```
;;;; META: Title: My First Wallace File
;;;; META: Author: Your Name
;;;; META: Version: 0.1.0

;;;; VERSION: 0.1.0 @beta #abc123
;;;; VERSION-CHANGES: Initial version

;;;; SYNOPSIS: This is where AI will help describe your code!

;;; SECTION: my-first-section
;; TODO: Add some cool features here!
;; LINK: design-doc.md
Some code would go here...
;;; END: SECTION
```

## The Complete Wallace Toolkit

### 1. File Information (META)
Think of META as your file's ID card:
```
;;;; META: Title: My Project
;;;; META: Author: Your Name
;;;; META: Version: 1.0.0
;;;; META: Category: User Interface
;;;; META: Status: Beta
;;;; META: Language: Python
```

### 2. Version Tracking (VERSION)
Keep track of what changed and when:
```
;;;; VERSION: 1.2.0 @beta #abc123
;;;; VERSION-CHANGES: Added new login screen
```
Status can be:
- @alpha (early testing)
- @beta (feature complete, testing)
- @rc (release candidate)
- @stable (production ready)

### 3. Organizing Code (SECTION)
Group related code together:
```
;;; SECTION: user-interface
Your code here...
;;; END: SECTION

;;; SECTION: database
More code here...
;;; END: SECTION
```

### 4. Tasks and Plans (TODO)
Keep track of what needs doing:
```
;; TODO: Add error checking @priority=1
;; TODO: Update login page @effort=3days @cost=$500
;; TODO: Fix security bug @due=2024-12-25 @assignee=sarah
```

### 5. Problems to Fix (FIXME)
Mark issues that need attention:
```
;; FIXME: Crashes with empty input @priority=1
;; FIXME: Memory leak @impact=500MB
;; FIXME: Slow query @effort=2hrs
```

### 6. Connecting Things (LINK)
Connect related pieces of your project:
```
;; LINK: helper.js#error-handling
;; LINK: docs/api.md:42
;; LINK: issue:123 @status=active
;; LINK: git:abc123#security-fix
```

### 7. AI Insights (SYNOPSIS)
Let AI help you understand your code:
```
;;;; SYNOPSIS: This login module handles user authentication.
;;;; It's connected to the database and session management
;;;; systems. Currently showing signs of performance issues
;;;; during high load. Consider adding caching.
```

### 8. Legacy Comments (RETRO)
Keep track of historical context:
```
;; RETRO: [2023-05-15] Original notes from first version:
;; This was implemented as a quick fix but worked well
;; @author=previous-developer
```

### 9. Function Documentation (FUNC)
Document how functions work:
```
;; FUNC: calculate_total(items, tax_rate) -> float
;; PURE: yes
;; EFFECTS: none
;; COMPLEXITY: O(n)
;; THROWS: ValueError on negative tax_rate
```

### 10. Future Ideas (IDEA)
Record your bright ideas:
```
;; IDEA: Add dark mode @impact=medium
;; IDEA: Use AI for recommendations @difficulty=high
;; IDEA: Add export feature @category=feature
```

### 11. Review Requests (REVIEW)
Ask for feedback:
```
;; REVIEW: Security check needed @reviewer=security-team
;; REVIEW: Performance review @due=2024-12-01
;; REVIEW: Design patterns @type=architecture
```

### 12. Custom Extensions (TAG)
For future expansion:
```
;; TAG: METRIC: response_time=100ms
;; TAG: CUSTOM: your_special_tag
```

## Working with Numbers

Wallace understands different types of numbers:

### Time
```
;; TODO: Quick fix @effort=30mins
;; TODO: Major update @effort=2days
;; TODO: Long term project @effort=3months
```

### Money
```
;; TODO: Update service @cost=$1500
;; FIXME: Budget overflow @impact=$5000
```

### Percentages
```
;; TODO: Improve performance @target=99.9%
;; REVIEW: Coverage @minimum=85%
```

### Technical Metrics
```
;; FIXME: Memory leak @impact=500MB
;; TODO: Optimize @target=100ms
```

## Working with AI

The SYNOPSIS tag is special - it's where AI assistants help you understand your code. They'll analyze how everything works together and provide insights you might miss.

Example of AI analysis:
```
;;;; SYNOPSIS: User authentication module
;;;; - Critical path for system security
;;;; - Connected to database and session management
;;;; - Currently experiencing scaling issues above 10k users
;;;; - Uses deprecated encryption library (needs update)
;;;; - Main bottleneck during peak hours
;;;; - Affected by recent security patch #abc123
```

## Real-World Examples

### Starting a New Feature

```
;;;; META: Title: User Profile System
;;;; META: Author: Your Team
;;;; META: Version: 0.1.0

;;;; VERSION: 0.1.0 @beta #def456
;;;; VERSION-CHANGES: Initial profile implementation

;;;; SYNOPSIS: New user profile system handling basic
;;;; user information and preferences. Dependencies on
;;;; auth system and database. Ready for basic testing.

;;; SECTION: profile-management
;; FUNC: update_profile(user_id, data) -> bool
;; PURE: no
;; EFFECTS: database write
;; THROWS: ValidationError

;; TODO: Add avatar upload @effort=2days
;; TODO: Add preferences @priority=2 @cost=$800
;; FIXME: Validation too strict @priority=1

;; LINK: auth.js#user-validation
;; LINK: docs/profile-spec.md

;; IDEA: Add social media integration @impact=high

Your code here...
;;; END: SECTION
```

### Managing Bug Fixes

```
;;; SECTION: error-handling
;; RETRO: [2024-01-15] Previous error system was basic
;; FIXME: Error messages unclear @priority=1
;; TODO: Add error codes @effort=4hrs
;; REVIEW: Error handling @type=usability

;; FUNC: handle_error(error) -> str
;; PURE: yes
;; EFFECTS: none
;; COMPLEXITY: O(1)

Your code here...
;;; END: SECTION
```

## Tips for Success

1. **Stay Organized**
   - Group related code in SECTIONS
   - Keep your TODOs specific
   - Use LINK to show connections
   - Let AI help with SYNOPSIS

2. **Track Everything**
   - Use RETRO for historical notes
   - Document functions with FUNC
   - Record ideas with IDEA
   - Request reviews with REVIEW

3. **Be Specific**
   - Include effort estimates (@effort=2days)
   - Add due dates (@due=2024-12-25)
   - Specify costs (@cost=$500)
   - Set priorities (@priority=1)

4. **Work with AI**
   - Read the SYNOPSIS regularly
   - Update version information
   - Maintain clear connections
   - Keep documentation current

## Common Questions

### Q: How detailed should my comments be?
A: Be clear but concise. Include enough information for both humans and AI to understand the context and implications.

### Q: What if I make a mistake in the syntax?
A: Most Wallace tools will help catch syntax errors. Start simple and add more detail as you get comfortable.

### Q: How often should I update versions?
A: Update the VERSION tag whenever you make significant changes:
- Major (1.0.0): Big changes that might break things
- Minor (0.1.0): New features that don't break existing code
- Patch (0.0.1): Small fixes and improvements

### Q: How do I work with legacy code?
A: Use the RETRO tag to preserve important historical information when updating old code.

## Moving Forward

Remember, Wallace is about:
- Clear communication
- Good organization
- Efficient collaboration
- Project management
- AI assistance

Take it step by step:
1. Start with basic META and VERSION tags
2. Add SECTIONs to organize your code
3. Use TODO and FIXME for task management
4. Add LINKs to show relationships
5. Let AI help with SYNOPSIS
6. Add other tags as needed

## Need Help?

- Review the examples
- Start with simple projects
- Ask AI assistants for guidance
- Share what you learn

Welcome to the Wallace community! You're starting an exciting journey into a new way of working with code, managing projects, and collaborating with AI.

Copyright © 2024 Wallace Documentation
