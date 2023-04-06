import aiosqlite
import asyncio
from .models import User, NPC

database_name = "discordgpt.db"


db_lock = asyncio.Lock()


async def create_tables():
    async with aiosqlite.connect(database_name) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS npcs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                abbreviation TEXT NOT NULL UNIQUE,
                pre_prompt TEXT,
                post_prompt TEXT,
                description TEXT,
                display INTEGER NOT NULL DEFAULT 1
            );
        """)

        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_user_id TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL,
                npc_id INTEGER,
                FOREIGN KEY (npc_id) REFERENCES npcs (id)
            );
        """)

        await conn.commit()



async def add_npc(name, abbreviation, pre_prompt, post_prompt, description, display):
    async with aiosqlite.connect(database_name) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""
        INSERT INTO npcs (name, abbreviation, pre_prompt, post_prompt, description, display) VALUES (?, ?, ?, ?, ?);""",
                            (name, abbreviation, pre_prompt, post_prompt, description, display))

        await conn.commit()


async def get_all_npcs():
    async with aiosqlite.connect(database_name) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""
            SELECT id, name, abbreviation, pre_prompt, post_prompt, description, display FROM npcs;
        """)

        npc_tuples = await cursor.fetchall()
        npc_list = [NPC(*npc_tuple) for npc_tuple in npc_tuples]

        return npc_list


async def add_user(discord_user_id, username):
    async with aiosqlite.connect(database_name) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""
            INSERT OR IGNORE INTO users (discord_user_id, username) VALUES (?, ?);
        """, (discord_user_id, username))

        await conn.commit()


async def update_user_npc(discord_user_id, selected_npc_id):
    async with aiosqlite.connect(database_name) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""
            UPDATE users SET npc_id = ? WHERE discord_user_id = ?;
        """, (selected_npc_id, discord_user_id))

        await conn.commit()


async def get_user_npc(discord_user_id):
    async with aiosqlite.connect(database_name) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""
            SELECT npcs.* FROM users
            JOIN npcs ON users.npc_id = npcs.id
            WHERE users.discord_user_id = ?;
        """, (discord_user_id,))

        npc_tuple = await cursor.fetchone()

        if npc_tuple:
            return NPC(*npc_tuple)
        else:
            return None

if __name__ == "__main__":
    asyncio.run(create_tables())
