import time

from numpy import exp
from .embeddings import generate_text_embeddings


class User:
    def __init__(self, id, discord_user_id, username, npc_id):
        self.id = id
        self.discord_user_id = discord_user_id,
        self.username = username,
        self.npc_id = npc_id

    def __repr__(self):
        return f"<User(id={self.id}, discord_user_id={self.discord_user_id}, username={self.username}, npc_id={self.npc_id})>"


class NPC:
    def __init__(self, id, name, abbreviation, pre_prompt, post_prompt, description, display):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.pre_prompt = pre_prompt
        self.post_prompt = post_prompt
        self.description = description
        self.display = display

    def __repr__(self):
        return f"<NPC(id={self.id}, name={self.name}, abbreviation={self.abbreviation}, pre_prompt={self.pre_prompt}, post_prompt={self.post_prompt}, description={self.description})>"


class Memory:
    def __init__(
            self,
            id,
            channel_id,
            user,
            message,
            creation_timestamp=None,
            last_accessed_timestamp=None,
            embeddings=None
    ):
        self.id = id
        self.user = user
        self.description = f"{user}: {message}"
        self.creation_timestamp = creation_timestamp if creation_timestamp else time.time()
        self.last_accessed_timestamp = last_accessed_timestamp if last_accessed_timestamp else time.time()
        self.channel_id = channel_id
        self.embeddings = embeddings if embeddings else generate_text_embeddings(
            self.description)
        self.recency_score = 0

    def __repr__(self):
        return f"<Memory(id={self.id}, user={self.user} description={self.description}, creation_timestamp={self.creation_timestamp}, last_accessed_timestamp={self.last_accessed_timestamp}, channel_id={self.channel_id})>"
