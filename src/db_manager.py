import aiosqlite
import asyncio

database_name = "discordgpt.db"


db_lock = asyncio.Lock()


async def init_db():
    global conn
    conn = await aiosqlite.connect(database_name)
    await create_tables()


async def create_tables():
    global conn
    cursor = await conn.cursor()

    await cursor.execute("""
        CREATE TABLE IF NOT EXISTS npcs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            abbreviation TEXT NOT NULL UNIQUE,
            pre_prompt TEXT,
            post_prompt TEXT,
            description TEXT
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


async def add_npc(name, abbreviation, pre_prompt, post_prompt, description):
    global conn
    cursor = await conn.cursor()

    await cursor.execute("""
    INSERT INTO npcs (name, abbreviation, pre_prompt, post_prompt, description) VALUES (?, ?, ?, ?, ?);""",
                         (name, abbreviation, pre_prompt, post_prompt, description))

    await conn.commit()


async def get_all_npcs():
    global conn
    cursor = await conn.cursor()

    await cursor.execute("""
        SELECT id, name, abbreviation, description FROM npcs;
    """)

    return await cursor.fetchall()


async def add_user(discord_user_id, username):
    global conn
    cursor = await conn.cursor()

    await cursor.execute("""
        INSERT OR IGNORE INTO users (discord_user_id, username) VALUES (?, ?);
    """, (discord_user_id, username))

    await conn.commit()


async def update_user_npc(discord_user_id, selected_npc_id):
    global conn
    cursor = await conn.cursor()

    await cursor.execute("""
        UPDATE users SET npc_id = ? WHERE discord_user_id = ?;
    """, (selected_npc_id, discord_user_id))

    await conn.commit()


async def get_user_npc(discord_user_id):
    global conn
    cursor = await conn.cursor()

    await cursor.execute("""
        SELECT npcs.* FROM users
        JOIN npcs ON users.npc_id = npcs.id
        WHERE users.discord_user_id = ?;
    """, (discord_user_id,))

    return await cursor.fetchone()

if __name__ == "__main__":
    asyncio.run(create_tables())
