from tokenizers import Tokenizer, pre_tokenizers, decoders, processors
import os
from .models import *
from .db_manager import *
from .logger import get_logger
from .embeddings import *

logger = get_logger(__name__)

# Initialize a tokenizer to count tokens
current__file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current__file_path)
tokenizer_file_path = os.path.join(
    current_directory, '..', 'tokenizer', 'tokenizer-wiki.json')

tokenizer = Tokenizer.from_file(tokenizer_file_path)
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=True)
tokenizer.decoder = decoders.ByteLevel()
tokenizer.post_processor = processors.TemplateProcessing(
    single="$0", special_tokens=[("[CLS]", 0), ("[SEP]", 1)]
)


async def add_message_to_context(channel_id, user, message):
    memory = Memory(None, channel_id, user, message)
    await add_memory(memory)
    logger.info(f"Added memory to the database: {memory}")


async def get_contex_by_channel(channel_id, prompt):
    memories = await get_memories_by_channel(channel_id)

    prompt_embeddings = generate_text_embeddings(prompt)

    scored_memories = []
    for memory in memories:
        recency_score = calculate_recency_score(memory)
        relevance_score = cosine_similarity(
            prompt_embeddings, memory.embeddings)
        combined_score = recency_score + relevance_score
        scored_memories.append((memory, combined_score))

    scored_memories.sort(key=lambda x: x[1], reverse=True)

    selected_memories = select_top_memories(scored_memories)

    descriptions = [memory.description for memory in selected_memories]
    context = "\n".join(descriptions)
    return context


def select_top_memories(scored_memories, max_tokens=1500):
    selected_memories = []
    current_token_count = 0

    for memory, _ in scored_memories:
        memory_token_count = len(tokenizer.encode(memory.description).tokens)

        if current_token_count + memory_token_count <= max_tokens:
            selected_memories.append(memory)
            current_token_count += memory_token_count
        else:
            break

    return selected_memories


async def get_remaining_tokens(channel_id, token_limit):
    memories = await get_memories_by_channel(channel_id)
    context_tokens = sum(len(tokenizer.encode(str(memory)))
                         for memory in memories)

    remaining_tokens = token_limit - context_tokens - 400

    logger.debug(f"Memories: {memories}")
    logger.debug(f"context_tokens: {context_tokens}")

    return remaining_tokens
