import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from src.response import generate_response
from src.utils.string_utils import split_string_list, re_clean
from src.logger import get_logger
from requests.exceptions import RequestException
import src.channel_context_manager as ccm
from src.custom_prompts import npcs

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


@bot.command()
async def gpt(cmd_ctx, *args):
    content = " ".join(args)

    if "--npc" in args:
        # Implement NPC flag
        pass
    else:
        channel_id = cmd_ctx.channel.id
        user = cmd_ctx.author

        ccm.add_message_to_context(channel_id, str(cmd_ctx.author), content)

        logger.info(
            f"Received message from {cmd_ctx.author} in channel {cmd_ctx.channel}: {content}")
        logger.debug(f"Channel type: {cmd_ctx.channel.type}")

        token_limit = ccm.get_remaining_tokens(channel_id, 4097)

        try:
            response = generate_response(
                content, channel_id, token_limit, user)
        except RequestException as e:
            response = "I'm sorry, but I encoutnered an error while processing your request. Please try again later."
            logger.exception("Error generating response")

        ccm.add_message_to_context(channel_id, str(bot.user), response)

        split_message = split_string_list([response])
        for msg in split_message:
            await cmd_ctx.send(re_clean(msg))
            logger.info(
                f"Sent message to {cmd_ctx.author} in channel {cmd_ctx.cannel}: {content}")


bot.run(discord_token)
