import argparse

from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import json
import openroutertest
from openroutertest import AI_semantic_update, GenerateHypothesisTests

properties = []

# Output containers
structure = {
    "functions": [],
    "branches": [],
    "loops": [],
    "returns": []
}

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

def main(file):
    global properties
    global structure
    
    PY_LANG = Language(tspython.language())

    # Initialize parser
    parser = Parser(PY_LANG)
    file_path = "dataset/python_programs/"+file
    # Load Python file
    code = open(file_path, "rb").read()
    tree = parser.parse(code)
    root = tree.root_node
    
    walk(root)
    print("\n=== STRUCTURE ===")
    #print(json.dumps(structure, indent=2))

    print("\n=== SEMANTIC PROPERTIES ===")
    #print(json.dumps(properties, indent=2))

    print("\n=== AI ===")
    properties = AI_semantic_update(file_path, properties)
    propertyfileName = file.split(".")[0]+".json"
    with open("properties/test_" + propertyfileName, "w", encoding="utf-8") as f:
        json.dump(properties, f, indent=2)

    print("=== NEW PROPS ===\n")
    #print(json.dumps(properties, indent=2))

    print("=== GENERATE HYPOTHESIS TESTS ===\n")
    hypothesisTests = GenerateHypothesisTests(file_path,properties)

    print("=== SAVING TESTS AS FILE ===\n")
    with open("tests/test_"+file,"w",encoding="utf-8") as f:
        f.write(str(hypothesisTests))
        
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--testFile", default=None, help="test file in dataset/python_programs")
    
    args = p.parse_args()
    
    if args.testFile is None:
        print("testFile argument is null.")
        exit(1)
        
    main(args.testFile)