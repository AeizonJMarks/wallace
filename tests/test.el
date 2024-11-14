;;;; META: Title: Elisp Test File
;;;; META: Version: 0.1.0
;;;; META: Author: Test Suite

;;;; SYNOPSIS: Test file for Elisp comment syntax.
;;;; SYNOPSIS: Tests multi-line continuation and error cases.

;;;; SECTION: valid-cases @0.1.0
;;;; TODO: Simple one-line todo item

;;;; REVIEW: Multi-line review item
;;;;        with proper continuation
;;;;        showing indentation

;;;; FIXME: Item with embedded period. Still continues.
;;;;        Because period is in continuation.

;; Invalid cases that should be caught:
; META: Wrong prefix (single semicolon)
;;;META: Wrong spacing (no space after semicolons)
;;;; meta: Lowercase tag name
;;;; META:Missing space after colon
;;;;META: Wrong spacing before tag
;;;; MET@: Invalid characters in tag
;;;; META: Tag with period ends here. New content.
