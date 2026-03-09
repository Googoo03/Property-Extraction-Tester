import requests
from extractJSON import getOutputText

#Function that updates the structure JSON with AI generate preconditions, conditions, and formal definitions
def AI_semantic_update(file_path, properties):
    #Convert structure dict to string
    properties_str = str(properties)

    #convert python file being tested  to string
    try:
        # Open the file in read mode ('r') with a context manager
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content into a string
            file_content = file.read()

        print("="*50+"\n"+file_path+"\n"+"="*50)
        print(file_content)
        print("="*50)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    #create user input here:
    user_input = file_content+"\n I am testing this python file, update or add the preconditions, conditions, and formal definitions for each test case in this JSON file and return to me just the JSON. The formal definition should be a python expression. In the formal definition, an 'output' should be the function under test called with base parameters:\n"+properties_str

    #call api. Inputs the user_input as a chat prompt for LLM
    data = apicall(user_input)
    dataJSON = data.json()

    #Gets the response from the agent
    print("Agent:\n")
    outputText = getOutputText(data)

    return outputText

def GenerateHypothesisTests(file_path,properties):
    #Convert structure dict to string
    properties_str = str(properties)
    
    #Generate a python file to run hypothesis tests
    with open('hypothesisPrompt.txt', 'r') as f:
        prompt = f.read().strip()
        
    #convert python file being tested  to string
    try:
        # Open the file in read mode ('r') with a context manager
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content into a string
            file_content = file.read()

        print("="*50+"\n"+file_path+"\n"+"="*50)
        print(file_content)
        print("="*50)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    user_input = "Here is the current python function. \n"+file_content+"\n" + prompt + "\n" + properties_str
    #call api
    data = apicall(user_input)
    
    return getOutputText(data)


#Function that writes the API call to Open Router and returns the request
def apicall(user_input):

    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()

    response = requests.post(
        "https://openrouter.ai/api/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "arcee-ai/trinity-large-preview:free",
            "input": user_input
        }
    )

    return response