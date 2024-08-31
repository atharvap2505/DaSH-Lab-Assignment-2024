import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('api_key')
api_url = 'https://api.groq.com/openai/v1/chat/completions'
model = 'gemma2-9b-it'  
source = "Gemma"

input_file = 'input.txt'
with open(input_file, 'r') as file:
    inputs = file.readlines()

output = []

def clean_response(text):
    text = text.strip()
    return text

for i, text in enumerate(inputs):
    time_sent = int(time.time())

    payload = {
        'model': model,  #Include the model in the payload
        'messages': [{'role': 'user', 'content': text.strip()}],
        'max_tokens': 2048  #Customize as needed
    }
    response = requests.post(api_url, headers={'Authorization': f'Bearer {api_key}'}, json=payload)
    time_recvd = int(time.time())

    if response.status_code == 200:
        result = response.json()
        response = clean_response(result.get('choices', [{}])[0].get('message', {}).get('content', 'No response'))
    else:
        response = f"Error: {response.status_code} - {response.text}"

    output.append({
        "Prompt": text.strip(),
        "Number" : i,
        "Message": response,
        "TimeSent": time_sent,
        "TimeRecvd": time_recvd,
        "Source": source
    })

output_file = 'output.json'
with open(output_file, 'w') as outfile:
    json.dump(output, outfile, indent=4)

print(f'Output saved to {output_file}')
