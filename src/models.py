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
