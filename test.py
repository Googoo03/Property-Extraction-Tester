from tree_sitter import Language

Language.build_library(
    # Output path
    'build/my-languages.so',
    # Paths to language repos
    ['tree-sitter-python']
)