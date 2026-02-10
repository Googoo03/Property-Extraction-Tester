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
structure = {
    "functions": [],
    "branches": [],
    "loops": [],
    "returns": []
}

properties = []


# Utility: get node text
def text(node):
    return code[node.start_byte:node.end_byte].decode()

def append_to_properties():
    properties.append({
        "scope": "branch",
        "function": "normalize",
        "property": "preserves_length",
        "formal": "len(output) == len(xs)"
    })

def get_if_statements(node, current_function):
    cond = node.child_by_field_name("condition")
    condition_text = cond.text.decode()
    structure["branches"].append(condition_text)

    # Branch-level property
    properties.append({
        "scope": "branch",
        "function": current_function,
        "condition": condition_text,
        "property": "branch_specific_behavior",
        "formal": "output behavior depends on condition"
    })

def get_functions(node):
    name_node = node.child_by_field_name("name")
    func_name = name_node.text.decode()
    structure["functions"].append(func_name)

    # Function-level property
    properties.append({
        "scope": "function",
        "function": func_name,
        "property": "preserves_length",
        "formal": "len(output) == len(input)"
    })



def walk(node, current_function=None):
    # Detect function definitions
    if node.type == "function_definition":
        get_functions(node)
        name_node = node.child_by_field_name("name")
        func_name = name_node.text.decode()
        current_function = func_name

    # Detect IF branches
    if node.type == "if_statement":
        get_if_statements(node, current_function)

    # Detect loops
    if node.type in ("for_statement", "while_statement", "list_comprehension"):
        structure["loops"].append(node.type)

        # Loop invariant property
        properties.append({
            "scope": "loop",
            "function": current_function,
            "property": "loop_invariant",
            "formal": "iteration preserves semantic rule"
        })

    # Detect return statements
    if node.type == "return_statement":
        return_text = node.text.decode()
        structure["returns"].append(return_text)

        # Post-condition property
        properties.append({
            "scope": "return",
            "function": current_function,
            "property": "return_postcondition",
            "formal": f"returns value satisfying expected semantics: {return_text}"
        })

    # Recurse
    for child in node.children:
        walk(child, current_function)
        
walk(root)
print("\n=== STRUCTURE ===")
print(json.dumps(structure, indent=2))

print("\n=== SEMANTIC PROPERTIES ===")
print(json.dumps(properties, indent=2))