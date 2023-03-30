import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from response import generate_response
from utils.string_utils import split_string_list

# Get API keys and tokens
load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

# Set up the bot with the required intents and command prefix
intents = Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    print(
        f"Received message from {message.author} in channel {message.channel}: {message.content}")
    print(f"Channel type: {message.channel.type}")

    if message.content.startswith('!gpt'):
        prompt = message.content[5:]
        response = generate_response(prompt)
        split_message = split_string_list([response])
        for msg in split_message:
            await message.channel.send(msg)
            print(
                f"Sent message to {message.author} in channel {message.channel}: {message.content}")

bot.run(discord_token)
