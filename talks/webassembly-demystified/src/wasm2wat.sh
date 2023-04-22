wasm2wat --generate-names -f "$1" | pygmentize -l wast -P style=rrt
