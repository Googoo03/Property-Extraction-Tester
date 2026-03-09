import json
from tokenize import String

#helper function to search the json for output -> message -> content -> text
#it is assumed that openrouter does this format for all - may need revisions in the future
def getOutputText(response):
    text = extract_text_from_response(response)
    text = clean_llm_text(text)
    
    print(response)
    
    parsedText = parse_json_safely(text)
    
    if parsedText is None:
        print("Assuming text or code")
        return text
    
    return parsedText
    
def extract_text_from_response(response):
    if response.status_code != 200:
        print("HTTP error:", response.status_code)
        print(response.text)
        return None

    data = response.json()
    output = data.get("output", [])

    texts = []

    for item in output:
        if item.get("type") != "message":
            continue

        for content in item.get("content", []):
            if content.get("type") == "output_text":
                texts.append(content.get("text", ""))

    full_text = "".join(texts).strip()

    if not full_text:
        print("No assistant text found.")
        print(data)
        return None

    return full_text

def clean_llm_text(text):
    text = text.strip()

    # remove markdown fences
    if text.startswith("```"):
        lines = text.splitlines()

        # remove first fence
        lines = lines[1:]

        # remove ending fence if present
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text

def parse_json_safely(text):
    text = clean_llm_text(text)

    # attempt direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # fallback: find first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    print("Could not parse JSON.")
    #print(text)
    return None