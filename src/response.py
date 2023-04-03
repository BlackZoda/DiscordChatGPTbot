import os
import aiohttp
from retry import retry
from dotenv import load_dotenv
from .logger import get_logger
from . import channel_context_manager as ccm
from .custom_prompts import load_prompt
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

logger = get_logger(__name__)


@retry(ConnectionError, tries=5, delay=2)
async def generate_response(prompt, channel_id, token_limit, user):

    context = ccm.read_context_from_file(channel_id)

    context += await load_prompt(str(user.id))

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
        "max_tokens": token_limit
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data) as response:
            if response.status == 200:
                message = (await response.json())["choices"][0]["message"]["content"].strip()
                return message
            else:
                error_message = (await response.json()).get("error", {}).get("message", "Unknown error")
                logger.error(
                    f"Error: Received status code {response.status}. Message: {error_message}")
                return "Sorry, I couldn't generate a response."
