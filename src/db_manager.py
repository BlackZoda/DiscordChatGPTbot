import sqlite3

database_name = "discordgpt.db"


def create_tables():
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS npcs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                abbreviation TEXT NOT NULL UNIQE,
                pre_prompt TEXT,
                post_prompt TEXT,
                description TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_user_id TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL,
                selected_npc_id INTEGER,
                FOREIGN KEY (selected_npc_id) REFERENCES npcs (id)
            )
        """)

        conn.commit()


def add_npc(name, abbrevation, pre_prompt, post_prompt, description):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.commit()

        cursor.execute("""
        INSERT INTO npcs (name, pre_prompt, post_promt) VALUES (?, ?, ?);""",
                       (name, pre_prompt, post_prompt))

        conn.commit()


def fetch_all_npcs():
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, abbreviation FROM npcs;
        """)

        npcs = cursor.fetchall()

    return npcs


def add_user_if_not_exists(discord_user_id, username):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO users (discord_user_id, username) VALUES (?, ?);
        """, (discord_user_id, username))


def add_user(discord_user_id, username, selected_npc_id=None):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (discord_user_id, username, selected_npc_id) VALUES (?, ?, ?);
        """)

        conn.commit()


def update_user_npc(discord_user_id, selected_npc_id):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET selected_npc_id = ? WHERE discord_user_id = ?;
        """, (selected_npc_id, discord_user_id))

    conn.commit()


def get_selected_npc(discord_user_id):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT npcs.* FROM users
            JOIN npcs ON users.selected_npc_id = npc.id
            WHERE users.discord_user_id = ?;
        """, (discord_user_id,))

        npc = cursor.fetchone()

    return npc


create_tables()
