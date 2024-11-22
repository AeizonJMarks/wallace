// Missing proper META and SYNOPSIS blocks

//// meta: Invalid lowercase
/// META: Wrong prefix level
//// META:Missing space after colon
///// META: Too many slashes

/// SECTION: incomplete-section
// Missing proper closure
const testFunction = () => {
    return true;
}
// Missing END tag

// Invalid continuation
//// TODO: Multi-line
/// continuation with wrong prefix

//// METRICS: invalid format 90
/// REVIEW:Wrong prefix level
