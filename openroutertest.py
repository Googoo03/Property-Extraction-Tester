import requests
import json

response = requests.post(
    'https://openrouter.ai/api/v1/responses',
    headers={
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openrouter/pony-alpha',
        'input': 'Hello, world!',
    }
)

print(json.dumps(response.json(), indent=2))
print(response.json().output.text())