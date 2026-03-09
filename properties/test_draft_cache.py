[
  {
    "scope": "function",
    "function": "draft_cache",
    "property": "preserves_length",
    "formal": "len(entries) == len(entries)"
  },
  {
    "scope": "branch",
    "function": "draft_cache",
    "condition": "key not in entries",
    "property": "branch_specific_behavior",
    "formal": "output is None"
  },
  {
    "scope": "branch",
    "function": "draft_cache",
    "condition": "now > expires_at",
    "property": "branch_specific_behavior",
    "formal": "output is None"
  },
  {
    "scope": "return",
    "function": "draft_cache",
    "property": "return_postcondition",
    "formal": "output is None or output == entries[key][0]"
  }
]