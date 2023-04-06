from .db_manager import add_user, update_user_npc, get_all_npcs, get_user_npc
from .logger import get_logger
from .utils.discord_utils import generate_table

logger = get_logger(__name__)


async def npc(cmd_ctx, user, user_id, args):
    await add_user(str(user_id), str(user))

    npc_flag_index = args.index("--npc")

    if len(args) > npc_flag_index + 1:
        selected_npc_abbr = args[npc_flag_index + 1]
        logger.info(f"NPC abbreviation provided: {selected_npc_abbr}")

        if selected_npc_abbr.lower() == "--clear":
            await update_user_npc(str(user_id), None)
            await cmd_ctx.send("Cleared NPC selection.")

        if selected_npc_abbr.lower() == "--list":
            npcs = await get_all_npcs()
            displayable_npcs = [npc for npc in npcs if npc.display]

            header = ["Abbr", "Name"]
            npc_list = [[npc.abbreviation, npc.name]
                        for npc in displayable_npcs]

            table = generate_table(header, npc_list)
            await cmd_ctx.send(f"```Available NPCs:\n{table}\n```")
            return

        npcs = await get_all_npcs()

        logger.debug(f"All NPCs: {npcs}")
        logger.debug(
            f"Searching for NPC with abbrevation: {selected_npc_abbr.lower()}")

        for npc in npcs:
            logger.debug(f"Checking NPC: {npc.abbreviation} ({npc.name})")
            if npc.abbreviation.lower() == selected_npc_abbr.lower():
                await update_user_npc(str(user_id), npc.id)
                await cmd_ctx.send(f"{str(user.name)} selected NPC: **{npc.name}**")
                return

        await cmd_ctx.send("No NPC found with the provided abbreviation.")
    else:
        selected_npc = await get_user_npc(str(user_id))

        if not selected_npc:
            await cmd_ctx.send("No NPC selected.")
        else:
            await cmd_ctx.send(f"Current NPC: **{selected_npc.name}**")
        await cmd_ctx.send("Please provide an NPC abbreviation to choose a new NPC, or use `--npc --list` to see all available NPCs.")
