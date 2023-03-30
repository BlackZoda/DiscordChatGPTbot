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


def split_string_list(strings, max_length=1990):
    result = []
    current_chunk = ""

    for text in strings:
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 1 <= max_length:
                if current_chunk:
                    current_chunk += "\n"
                current_chunk += paragraph
            else:
                result.append(current_chunk.strip())
                current_chunk = paragraph

    if current_chunk:
        result.append(current_chunk.strip())

    return result


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
        # Wrap the response string in a list
        split_message = split_string_list([response])
        for msg in split_message:  # Replace 'message' with 'msg' to avoid confusion
            # Remove 'list' since split_message is already a list
            await message.channel.send(msg)
            print(
                f"Sent message to {message.author} in channel {message.channel}: {message.content}")

    # await bot.process_commands(message)

# Run the bot
bot.run(discord_token)  # Insert DISCORD_TOKEN here
