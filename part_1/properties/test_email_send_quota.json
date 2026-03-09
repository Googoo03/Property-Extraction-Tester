[
  {
    "scope": "function",
    "function": "email_send_quota",
    "property": "preserves_length",
    "formal": "len(recent) <= len(sent)"
  },
  {
    "scope": "loop",
    "function": "email_send_quota",
    "property": "loop_invariant",
    "formal": "all(t >= cutoff for t in recent)"
  },
  {
    "scope": "branch",
    "function": "email_send_quota",
    "condition": "len(recent) > limit",
    "property": "branch_specific_behavior",
    "formal": "output == False if len(recent) > limit else output == True"
  },
  {
    "scope": "return",
    "function": "email_send_quota",
    "property": "return_postcondition",
    "formal": "output == False if len(recent) > limit else output == True"
  }
]