import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from response import generate_response
from utils.string_utils import split_string_list
from utils.string_utils import re_clean
from logger import get_logger
import channel_context_manager as ccm

# General setup and keys
load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

logger = get_logger(__name__)

# Set up the bot with the required intents and command prefix
intents = Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Bot is ready! Logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    channel_id = message.channel.id
    content = message.content
    if content.startswith('!gpt'):
        content = content[5:].strip()
    ccm.add_message_to_context(
        channel_id, str(message.author), content)
    ccm.trim_context_to_token_limit(channel_id, 1800)

    logger.info(
        f"Received message from {message.author} in channel {message.channel}: {message.content}")
    logger.debug(f"Channel type: {message.channel.type}")

    if message.content.startswith('!gpt'):

        token_limit = ccm.get_remaining_tokens(channel_id, 4000)
        response = generate_response(content, channel_id, token_limit)

        # Add the bot's response to the context
        ccm.add_message_to_context(channel_id, str(bot.user), response)

        split_message = split_string_list([response])
        for msg in split_message:
            await message.channel.send(re_clean(msg))
            logger.info(
                f"Sent message to {message.author} in channel {message.channel}: {message.content}")


bot.run(discord_token)
