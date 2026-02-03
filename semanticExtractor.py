from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import json

PY_LANG = Language(tspython.language())

# Initialize parser
parser = Parser(PY_LANG)

# Load Python file
code = open("dataset/python_programs/ad_mix.py", "rb").read()
tree = parser.parse(code)
root = tree.root_node

# Output containers
functions = []
classes = []
imports = []
calls = []
assignments = []
branches = []
loops = []
side_effects = []
dangerous = []
definitions = set()
uses = set()

# Utility: get node text
def text(node):
    return code[node.start_byte:node.end_byte].decode()

# Walk Tree-Sitter CST
def walk(node):
    node_type = node.type

    # Functions
    if node_type == "function_definition":
        name = node.child_by_field_name("name")
        if name:
            functions.append(text(name))

    # Classes
    if node_type == "class_definition":
        name = node.child_by_field_name("name")
        if name:
            classes.append(text(name))

    # Imports
    if node_type in ("import_statement", "import_from_statement"):
        imports.append(text(node))

    # Assignments
    if node_type == "assignment":
        lhs = node.child_by_field_name("left")
        rhs = node.child_by_field_name("right")
        if lhs:
            assignments.append(text(lhs))
            definitions.add(text(lhs))
        if rhs:
            uses.add(text(rhs))

    # Function calls
    if node_type == "call":
        fn = node.child_by_field_name("function")
        if fn:
            fn_name = text(fn)
            calls.append(fn_name)

            # Side effect detection
            if fn_name in ("open", "print"):
                side_effects.append(("io", fn_name))
            if "requests" in fn_name or "socket" in fn_name:
                side_effects.append(("network", fn_name))
            if "subprocess" in fn_name:
                side_effects.append(("subprocess", fn_name))

            # Dangerous ops
            if fn_name in ("eval", "exec"):
                dangerous.append(fn_name)

    # Branching (CFG hint)
    if node_type in ("if_statement", "try_statement"):
        branches.append(text(node))

    # Loops
    if node_type in ("for_statement", "while_statement"):
        loops.append(text(node))

    # Identifier usage
    if node_type == "identifier":
        uses.add(text(node))

    for c in node.children:
        walk(c)

walk(root)

# Build call graph edges
call_graph = [{"caller": f, "calls": calls} for f in functions]

# Semantic summary JSON
output = {
    "functions": sorted(set(functions)),
    "classes": sorted(set(classes)),
    "imports": imports,
    "assignments": assignments,
    "definitions": list(definitions),
    "uses": list(uses),
    "call_graph": call_graph,
    "branches": len(branches),
    "loops": len(loops),
    "side_effects": side_effects,
    "dangerous_calls": dangerous
}

print(json.dumps(output, indent=2))
