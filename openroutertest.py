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
    print("User:\n"+user_input)

    #call api. Inputs the user_input as a chat prompt for LLM
    data = apicall(user_input)
    dataJSON = data.json()
    # Line below prints entire API request
    # print(json.dumps(data, indent=2))

    #Gets the response from the agent
    print("Agent:\n")
    outputText = getOutputText(data)
    for text in outputText:
        print(text)

    return outputText

def GenerateHypothesisTests(properties):
    #Convert structure dict to string
    properties_str = str(properties)
    
    #Generate a python file to run hypothesis tests
    user_input = "I am using hypothesis to perform tests on python functions. Please make a dedicated hypothesis test for each semantic property in this included JSON format. Return to me only the completed python file. Assume hypothesis and pytest are already installed. Assume the tested function is found in dataset\python_programs\**insert function name**. As a decorator, please do NOT include '@settings(suppress_health_check=[HealthCheck.too_slow])'.\n" + properties_str
    
    #call api
    data = apicall(user_input)
    
    #print(json.dumps(getOutputText(data), indent=2))
    
    return getOutputText(data)


#Function that writes the API call to Open Router and returns the request
def apicall(user_input):
    
    #no point in doing an entire API call if empty prompt
    if user_input == "":
        return None
    
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
    
    response = requests.post(
        'https://openrouter.ai/api/v1/responses',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'openrouter/aurora-alpha',
            'input': user_input,
        }
    )
    return response