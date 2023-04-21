import asyncio
import os
import pickle
import time
import aiosqlite
import openai
from dotenv import load_dotenv
import numpy as np

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

database_name = "discordgpt.db"


def generate_text_embeddings(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def calculate_recency_score(memory, current_time=None):
    if current_time is None:
        current_time = time.time()
    time_elapsed = current_time - memory.creation_timestamp
    decay_factor = 0.99
    recency = np.exp(-time_elapsed * (1-decay_factor))
    return recency


def cosine_similarity(vector1, vector2):
    if isinstance(vector1, bytes):
        vector1 = pickle.loads(vector1)
    if isinstance(vector2, bytes):
        vector2 = pickle.loads(vector2)

    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm1 * norm2)
    return similarity


async def populate_database_embeddings():
    async with aiosqlite.connect(database_name) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""SELECT * FROM memories""")
        rows = await cursor.fetchall()

        for row in rows:
            description = row[3]
            embedding = generate_text_embeddings(description)
            embedded_bytes = pickle.dumps(embedding)
            await cursor.execute(
                """UPDATE memories SET embeddings=? WHERE id=?""", (embedded_bytes, row[0]))

        await conn.commit()

# asyncio.run(populate_database_embeddings())
