import requests
import json

#Function that updates the structure JSON with AI generate preconditions, conditions, and formal definitions
def AI_semantic_update(file_path, structure):
    #Convert structure dict to string
    structure_str = str(structure)

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
    user_input = file_content+"\n I am testing this python file, update or add the preconditions, conditions, and formal definitions for each test case in this JSON file:\n"+structure_str
    data = apicall(user_input).json()

    # Line below prints entire API request
    # print(json.dumps(data, indent=2))

    #Gets the response from the agent
    print(data['output'][0]['content'][0]['text'])
    return data['output'][0]['content'][0]['text']


#Function that writes the API call to Open Router and returns the request
def apicall(user_input):
    response = requests.post(
        'https://openrouter.ai/api/v1/responses',
        headers={
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'openrouter/aurora-alpha',
            'input': user_input,
        }
    )
    return response