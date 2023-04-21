import os
import aiohttp
from dotenv import load_dotenv
from .logger import get_logger
from . import channel_context_manager as ccm
from .custom_prompts import load_prompt
from .db_manager import get_user_npc
import os
from .utils.string_utils import re_clean_prompt

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

logger = get_logger(__name__)


async def generate_response(prompt, channel_id, user):

    prompt = re_clean_prompt(prompt)

    context, remaining_words = await ccm.get_context_by_channel(channel_id, prompt)

    npc = await get_user_npc(str(user.id))

    if npc is not None:
        context += await load_prompt(str(user.id), npc.name, str(user))
    else:
        context += ""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": remaining_words
    }

    print("Data:", data)

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
