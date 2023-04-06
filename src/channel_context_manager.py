from collections import deque, defaultdict
from tokenizers import Tokenizer, pre_tokenizers, decoders, processors
import os

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

# Create a dictionary to store recent messages in each channel
channel_context = defaultdict(deque)


def get_context_file_path(channel_id):
    return os.path.join(current_directory, '..', 'data', 'contexts', f'context_{channel_id}.txt')


def add_message_to_context(channel_id, user, message):
    new_entry = (user, message)
    channel_context[channel_id].append(new_entry)
    # Save the channel context to a text file in the 'channel_contexts' folder
    with open(get_context_file_path(channel_id), "w") as f:
        for user, msg in channel_context[channel_id]:
            f.write(f"{user}: {msg}\n")

    trim_context_to_token_limit(channel_id, 2000)


def trim_context_to_token_limit(channel_id: str, token_limit: int):
    context = get_context(channel_id)
    lines = context.split("\n")
    tokens = 0
    trimmed_lines = []

    for line in reversed(lines):
        line_tokens = len(tokenizer.encode(line).ids)
        tokens += line_tokens

        if tokens > token_limit:
            break

        trimmed_lines.insert(0, line)

    set_context(channel_id, "\n".join(trimmed_lines))


def get_context(channel_id):
    with open(get_context_file_path(channel_id), "r") as f:
        context = f.read()
    return context


def set_context(channel_id, context):
    with open(get_context_file_path(channel_id), "w") as f:
        f.write(context)


def read_context_from_file(channel_id):
    with open(get_context_file_path(channel_id), "r") as f:
        lines = f.readlines()

    context = ""

    for line in reversed(lines):
        context = line + context

    return context


def get_remaining_tokens(channel_id, token_limit):
    context_tokens = sum(
        len(tokenizer.encode(line)) for line in read_context_from_file(channel_id).splitlines()
    )

    return token_limit - context_tokens - 397
