import os
import aiohttp
from dotenv import load_dotenv
from .logger import get_logger
from . import channel_context_manager as ccm
from .custom_prompts import load_prompt
from .db_manager import get_user_npc
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

logger = get_logger(__name__)


async def generate_response(prompt, channel_id, token_limit, user):

    context = await ccm.get_contex_by_channel(channel_id, prompt)

    npc = await get_user_npc(str(user.id))

    if npc is not None:
        context += await load_prompt(str(user.id), npc.name, str(user))
    else:
        context += ""

    # logger.debug(context)

    max_content_length = 3500
    truncated_context = context[-max_content_length:]

    token_limit = min(4096, max(1, 4096 - len(truncated_context)))

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": truncated_context},
            {"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": token_limit
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
