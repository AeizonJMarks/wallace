#!/bin/zsh

#### META: TITLE A Wallace File Validator
#### META: VERSION 0.0.1
#### META: AUTHOR Claude & Human
#### META: CATEGORY Tools
#### TAGS: EXIT_CODES VALIDATION_STATES PURE EFFECTS THROWS

#### VERSION: 0.0.1 @alpha #initial
#### VERSION-CHANGES: Initial validator implementation

#### SYNOPSIS: Basic Wallace file validator for both .wal and embedded formats.
#### SYNOPSIS: Validates all core and extension tags against specification.
#### SYNOPSIS: Handles both semicolon (.wal) and language-specific comment formats.
#### SYNOPSIS: Provides detailed error reporting with line numbers.
#### END: SYNOPSIS

### SECTION: initialization @0.0.1
## TODO: Add more specific error codes @priority=2
exit_success=0
exit_no_file=1
exit_invalid_syntax=2
exit_malformed_meta=3

## TODO: Add validation for optional META keys @priority=3
required_meta=("TITLE" "VERSION" "AUTHOR")

## TODO: Add validation for tag attributes @priority=2
core_tags=("META:" "TAGS:" "VERSION:" "SECTION:" "TODO:" "FIXME:" "LINK:" "SYNOPSIS:" \
          "RETRO:" "FUNCTION:" "IDEA:" "REVIEW:" "TAG:" "END:")

### SECTION: utility-functions @0.0.1
## FUNCTION: get_comment_symbol(file) -> string
## PURE: yes
## EFFECTS: none
get_comment_symbol() {
    local file=$1
    case "${file:e}" in
        wal) echo ";;;;" ;;
        sh)  echo "####" ;;
        *)   echo ";;;;" ;; # Default to .wal format
    esac
}

### SECTION: validation-functions @0.0.1

## FUNCTION: collect_extensions(file) -> array
## PURE: no
## EFFECTS: reads file
collect_extensions() {
    local file=$1
    local comment=$(get_comment_symbol "$file")
    local extensions=()
    
    while IFS= read -r line; do
        if [[ $line =~ ^"$comment TAGS: "(.+) ]]; then
            local tags=(${(s: :)match[1]})
            for tag in $tags; do
                extensions+=("$tag:")
            done
        fi
    done < "$file"
    
    echo "${extensions[@]}"
}

## FUNCTION: validate_meta_block(file) -> bool
## PURE: no
## EFFECTS: reads file
validate_meta_block() {
    local file=$1
    local comment=$(get_comment_symbol "$file")
    local found_meta=0
    local meta_keys=()

    while IFS= read -r line; do
        if [[ $line =~ ^"$comment META: "([A-Z]+)' '.+ ]]; then
            found_meta=1
            meta_keys+=("${match[1]}")
        elif [[ $found_meta -eq 1 && ! $line =~ ^"$comment META: " ]]; then
            break
        fi
    done < "$file"

    # Check for required META keys
    for key in "${required_meta[@]}"; do
        if [[ ! " ${meta_keys[@]} " =~ " ${key} " ]]; then
            echo "Error: Missing required META key: $key"
            return 1
        fi
    done

    return 0
}

## FUNCTION: validate_tags(file) -> bool
## PURE: no
## EFFECTS: reads file
## THROWS: error messages to stdout
validate_tags() {
    local file=$1
    local comment_base=$(get_comment_symbol "$file")
    local comment_l3=${comment_base%#}
    local comment_l2=${comment_l3%#}
    local line_number=0
    local valid=0
    
    # Collect extensions first
    local extensions=($(collect_extensions "$file"))
    local valid_tags=("${core_tags[@]}" "${extensions[@]}")

    while IFS= read -r line; do
        ((line_number++))
        
        # Skip empty lines
        [[ -z "$line" ]] && continue
        
        # Check each level of comment depth
        if [[ $line =~ ^"$comment_base "([A-Z]+:)' '.+ ]]; then
            local tag=${match[1]}
            if [[ ! " ${valid_tags[@]} " =~ " ${tag} " ]]; then
                echo "Error: Invalid tag '$tag' at line $line_number"
                valid=1
            fi
        elif [[ $line =~ ^"$comment_l3 "([A-Z]+:)' '.+ ]]; then
            local tag=${match[1]}
            if [[ ! " ${valid_tags[@]} " =~ " ${tag} " ]]; then
                echo "Error: Invalid tag '$tag' at line $line_number"
                valid=1
            fi
        elif [[ $line =~ ^"$comment_l2 "([A-Z]+:)' '.+ ]]; then
            local tag=${match[1]}
            if [[ ! " ${valid_tags[@]} " =~ " ${tag} " ]]; then
                echo "Error: Invalid tag '$tag' at line $line_number"
                valid=1
            fi
        fi
    done < "$file"

    return $valid
}

### SECTION: main @0.0.1
## FUNCTION: main(args) -> int
## PURE: no
## EFFECTS: reads file, writes to stdout
main() {
    ## TODO: Add support for multiple file validation @priority=3
    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <wal-file>"
        exit $exit_no_file
    fi

    local file=$1

    ## FIXME: Add check for file type (wal vs source) @priority=1
    if [[ ! -f $file ]]; then
        echo "Error: File '$file' not found"
        exit $exit_no_file
    fi

    # Validate META block
    if ! validate_meta_block "$file"; then
        exit $exit_malformed_meta
    fi

    # Validate tags
    if ! validate_tags "$file"; then
        exit $exit_invalid_syntax
    fi

    echo "Success: File '$file' is Wallace compliant"
    exit $exit_success
}

## TODO: Add self-test functionality @priority=2
## IDEA: Add validation report generation
## IDEA: Consider adding --strict mode for additional checks

# Call main with all script arguments
main "$@"
