// Missing proper header block
//// meta: lowercase tag
///META: Invalid spacing
//// META:Missing space after colon
///// META: Too many slashes

/// SECTION: test-section
// Missing required header blocks
void test_function() {
    return;
}
/// END: SECTION: mismatched-name  // Section name mismatch

// Invalid tag formats
//// TODO Missing colon
//// METRICS Invalid format 100
/// REVIEW:Wrong prefix level
