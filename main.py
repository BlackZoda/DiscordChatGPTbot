import random
import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands, tasks
from src.logger import get_logger
from src.chat_message import process_request
from src.db_manager import create_tables
from src.npc import npc
import asyncio

# General setup

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

logger = get_logger(__name__)

intents = Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True


class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start(self, *args, **kwargs):
        tries = 5
        for i in range(tries):
            try:
                await super().start(*args, **kwargs)
                break
            except RuntimeError as e:
                if i < tries - 1:
                    wait_time = 2 ** i + random.uniform(0, 1)
                    await asyncio.sleep(wait_time)
                else:
                    raise e


bot = CustomBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Bot is ready! Logged in as {bot.user}")
    # await create_tables()


@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Error in event: {event}")
    logger.error(f"Error details: {args}, {kwargs}")

    # Wait for 30 seconds and attempt a reconnection
    await asyncio.sleep(30)
    await bot.connect(reconnect=True)


@bot.event
async def on_resumed():
    logger.info("Bot has reconnected")


@tasks.loop(seconds=60)  # task runs every 60 seconds
async def my_background_task(self):
    channel = self.get_channel(1089930955151638560)  # channel ID goes here
    await channel.send("Bot is still alive...")


@bot.command()
async def shutdown(ctx):
    if ctx.author.id == 553180464731652106:
        await ctx.send("Shutting down the bot...")
        await bot.close()


@bot.command()
async def gpt(cmd_ctx, *args):
    channel_id = cmd_ctx.channel.id
    user = cmd_ctx.author
    user_id = cmd_ctx.author.id

    if "--npc" in args:
        await npc(cmd_ctx, user, user_id, args)

    else:
        content = " ".join(args).replace('"', '\\"')
        await process_request(cmd_ctx, channel_id, content, user, bot)


@bot.event
async def on_disconnect():
    logger.info("Bot is disconnecting...")

bot.run(discord_token, reconnect=True)
