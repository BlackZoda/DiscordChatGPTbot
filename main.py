import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from src.logger import get_logger
from src.chat_message import process_request
# Correct the import
from src.db_manager import *

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
        await add_user(str(user_id), str(user))

        npc_flag_index = args.index("--npc")

        if len(args) > npc_flag_index + 1:
            selected_npc_abbr = args[npc_flag_index + 1]
            logger.info(f"NPC appreviation provided: {selected_npc_abbr}")

            if selected_npc_abbr.lower() == "--list":
                npcs = await get_all_npcs()
                header = f"| {'Abbr':<8} | {'Name':<18} |\n| {'-' * 8} | {'-' * 18} |"
                npc_list = "\n".join(
                    [f"| {npc[2]:<8} | {npc[1]:<18} |" for npc in npcs])
                await cmd_ctx.send(f"```Available NPCs:\n{header}\n{npc_list}```")
                return

            npcs = await get_all_npcs()
            for npc in npcs:
                if npc[2].lower() == selected_npc_abbr.lower():
                    await update_user_npc(str(user_id), npc[0])
                    await cmd_ctx.send(f"Selected NPC: **{npc[1]}**")
                    return

            await cmd_ctx.send("No NPC found with the provided abbreviation.")
        else:
            selected_npc = await get_user_npc(str(user_id))

            if not selected_npc:
                await cmd_ctx.send("No NPC selected.")
            else:
                npc_name = selected_npc[1]
                await cmd_ctx.send(f"Current NPC: **{npc_name}**")
            await cmd_ctx.send("Please provide an NPC abbreviation to choose a new NPC, or use `--npc --list` to see all available NPCs.")

    else:
        content = " ".join(args)
        await process_request(cmd_ctx, channel_id, content, user, bot)


@bot.event
async def on_disconnect():
    logger.info("Bot is disconnecting...")
    await conn.close()

bot.run(discord_token)
