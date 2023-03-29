import os
from dotenv import load_dotenv
import requests
from discord import Intents
from discord.ext import commands

# Get API keys and tokens
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
discord_token = os.getenv("DISCORD_TOKEN")

# Set up the bot with the required intents and command prefix
intents = Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


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


@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return

    print(
        f"Received message from {message.author} in channel {message.channel}: {message.content}")
    print(f"Channel type: {message.channel.type}")

    if message.content.startswith('!gpt'):
        prompt = message.content[5:]
        response = generate_response(prompt)
        await message.channel.send(response)

    # await bot.process_commands(message)

# Run the bot
bot.run(discord_token)  # Insert DISCORD_TOKEN here
