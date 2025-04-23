from openai import OpenAI

# Create client
client = OpenAI(
    api_key="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",
)

# Call ChatCompletion with the new client interface
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "introduce yourself"}
    ]
)

# Print the reply
print(response.choices[0].message.content)


#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