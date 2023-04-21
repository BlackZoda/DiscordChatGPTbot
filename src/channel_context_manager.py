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
    # logger.info(f"Added memory to the database: {memory}")


def select_most_recent_memories(memories, num_recent=5):
    recent_memories = sorted(
        memories, key=lambda x: x[0].creation_timestamp, reverse=True)[:num_recent]
    return recent_memories


async def get_context_by_channel(channel_id, prompt):
    memories = await get_memories_by_channel(channel_id)

    prompt_embeddings = generate_text_embeddings(prompt)

    scored_memories = []
    for memory in memories:
        recency_score = calculate_recency_score(memory)
        relevance_score = cosine_similarity(
            prompt_embeddings, memory.embeddings)
        alpha = 0.5
        combined_score = (alpha * relevance_score) + \
            ((1 - alpha) * recency_score)
        scored_memories.append(
            (memory, (combined_score, relevance_score, recency_score)))

    scored_memories.sort(key=lambda x: x[1][0], reverse=True)

    selected_memories, remaining_words = select_top_memories(scored_memories)
    most_recent_memories = select_most_recent_memories(scored_memories)

    combined_memories = list(
        {memory[0].id: memory for memory in selected_memories + most_recent_memories}.values())
    combined_memories.sort(key=lambda x: x[1][2], reverse=False)

    # selected_memories.sort(key=lambda x: x[1][2], reverse=False)

    descriptions = [memory[0].description.replace(
        f"{memory[0].user}:", "", 1) for memory in combined_memories]
    context = "\nChat log: [" + ";\n".join(descriptions) + "]\n"
    return context, remaining_words


def select_top_memories(scored_memories, max_words=1200):
    selected_memories = []
    word_count = 0

    for memory in scored_memories:
        memory_word_count = len(memory[0].description.split())

        if word_count + memory_word_count <= max_words:
            selected_memories.append(memory)
            word_count += memory_word_count
        else:
            break

    remaining_words = 2700 - word_count - 800

    logger.info(f"Remaining words: {remaining_words}")
    logger.info(f"Word count: {word_count}")

    return selected_memories, remaining_words
