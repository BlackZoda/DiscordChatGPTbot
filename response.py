import os
import requests
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        message = response.json()["choices"][0]["message"]["content"].strip()
        return message
    else:
        print(f"Error: Received status code {response.status_code}")
        return "Sorry, I couldn't generate a response."