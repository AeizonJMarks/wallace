#### META: Title: Valid Test Python File
#### META: Version: 0.1.0
#### META: Author: Test Suite
#### META: Path: ~/wallace/tests/valid.py

#### SYNOPSIS: This file demonstrates correct Wallace tag usage.
#### SYNOPSIS: All tags follow proper syntax and formatting rules.
#### SYNOPSIS: Used to validate the Wallace parser's success cases.

### SECTION: basic-tags @0.1.0

#### TODO: Implement new feature
####       with proper continuation
####       using correct prefix

#### FIXME: Fix performance issue in algorithm
####        using multiple lines to describe
####        the complete problem

### SECTION: metadata-examples @0.1.0

#### NOTE: Important implementation detail
####       that spans multiple lines
####       with proper indentation

#### REVIEW: Code review needed for this section
####         focusing on performance and
####         maintainability aspects

### SECTION: status-tracking @0.1.0

#### IDEA: Could implement caching
####       to improve performance
####       significantly

#### DONE: Completed initial implementation
####       with all required features
####       as specified

# Regular Python comments
# These should be ignored by Wallace
# But are fine to include

def some_python_code():
    # This demonstrates that Wallace tags
    # can coexist with normal code
    pass

### SECTION: complex-examples @0.1.0

#### TODO: Multi-part task with period handling.
####       This continues despite the period.
####       And keeps going properly.

#### LINK: references/design.md#architecture
####       with additional context
####       about the reference

### END: SECTION
