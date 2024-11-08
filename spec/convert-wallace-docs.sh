#!/bin/bash

FILES=("wallace-spec.md" "wallace-user-manual.md" "wallace-ai-manual.md")

for file in "${FILES[@]}"; do
    output="${file%.md}.pdf"
    echo "Converting $file to $output..."
    pandoc "$file" \
        -o "$output" \
        --pdf-engine=xelatex \
        -V geometry:margin=1in \
        -V mainfont="DejaVu Sans" \
        --toc \
        --toc-depth=2 \
        -V colorlinks=true
done

echo "Conversion complete!"
