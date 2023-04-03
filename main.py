import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from src.logger import get_logger
from src.chat_message import process_request
from src.db_manager import *
from src.npc import npc

# General setup

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

logger = get_logger(__name__)

intents = Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Bot is ready! Logged in as {bot.user}")
    await init_db()
    await create_tables()


@bot.command()
async def gpt(cmd_ctx, *args):
    channel_id = cmd_ctx.channel.id
    user = cmd_ctx.author
    user_id = cmd_ctx.author.id

    if "--npc" in args:
        await npc(cmd_ctx, user, user_id, args)

    else:
        content = " ".join(args)
        await process_request(cmd_ctx, channel_id, content, user, bot)


@bot.event
async def on_disconnect():
    logger.info("Bot is disconnecting...")
    await conn.close()

bot.run(discord_token)
