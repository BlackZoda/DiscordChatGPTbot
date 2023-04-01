import os
import requests
from retry import retry
from dotenv import load_dotenv
from logger import get_logger
import channel_context_manager as ccm
from channel_context_manager import tokenizer

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

logger = get_logger(__name__)


@retry(ConnectionError, tries=5, delay=2)
def generate_response(prompt, channel_id, token_limit):

    context = ccm.read_context_from_file(channel_id, 1800)

    prompt_tokens = tokenizer.encode(prompt).tokens

    context_tokens = len(tokenizer.encode(context))
    tokens_to_generate = token_limit - context_tokens - len(prompt_tokens) - 60

    if tokens_to_generate < 1:
        context = context[-(token_limit - len(prompt_tokens) - 10):]
        tokens_to_generate = token_limit - len(prompt_tokens) - 10

    print(f"\nContext: {context}\n")
    print(f"\nContext Length: {len(context)}\n")
    print(f"\nPrompt: {prompt}\n")
    print(f"\nPrompt length: {len(prompt)}\n")
    print(f"\nMax tokens: {tokens_to_generate}\n")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": tokens_to_generate
    }

    # print(f"\n{headers}\n \n{data}\n")

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        message = response.json()["choices"][0]["message"]["content"].strip()
        print(f"\nResponse Message: {message}\n")
        print(f"\nResponse Message Length: {len(message)}\n")
        return message
    else:
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        logger.error(
            f"Error: Received status code {response.status_code}. Message: {error_message}")
        return "Sorry, I couldn't generate a response."
