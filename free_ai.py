import requests
import json

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_TOKEN"}

# Create the request payload
data = {
  "inputs": "<s>[INST] introduce yourself [/INST]",
  "parameters": {"max_new_tokens": 100}
}

response = requests.post(API_URL, headers=headers, json=data)
result = response.json()

# Print the entire result to check structure
print(json.dumps(result, indent=4))

# Extract and print generated text
generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get('generated_text') or result
print("Generated Response:\n", generated_text)
