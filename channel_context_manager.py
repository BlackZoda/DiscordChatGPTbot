from collections import deque, defaultdict
from tokenizers import Tokenizer, models, pre_tokenizers, decoders, processors
from tokenizers.processors import TemplateProcessing
from logger import get_logger

# Initialize a tokenizer to count tokens

tokenizer = Tokenizer.from_file("./tokenizer/tokenizer-wiki.json")
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=True)
tokenizer.decoder = decoders.ByteLevel()
tokenizer.post_processor = processors.TemplateProcessing(
    single="$0", special_tokens=[("[CLS]", 0), ("[SEP]", 1)]
)

# Create a dictionary to store recent messages in each channel
channel_context = defaultdict(deque)


def add_message_to_context(channel_id, user, message):
    new_entry = (user, message)
    channel_context[channel_id].append(new_entry)

    # Save the channel context to a text file in the 'channel_contexts' folder
    with open(f"contexts/context_{channel_id}.txt", "w") as f:
        for user, msg in channel_context[channel_id]:
            f.write(f"{user}: {msg}\n")

    trim_context_to_token_limit(channel_id, 100)


def trim_context_to_token_limit(channel_id: str, token_limit: int):
    context = get_context(channel_id)
    lines = context.split("\n")
    tokens = 0
    trimmed_lines = []

    for line in reversed(lines):
        line_tokens = len(tokenizer.encode(line).ids)
        tokens += line_tokens

        print("Line tokens: " + str(line_tokens))
        print("Tokens: " + str(tokens))

        if tokens > token_limit:
            break

        trimmed_lines.insert(0, line)

    set_context(channel_id, "\n".join(trimmed_lines))


def get_context(channel_id):
    with open(f"contexts/context_{channel_id}.txt", "r") as f:
        context = f.read()
    return context


def set_context(channel_id, context):
    with open(f"contexts/context_{channel_id}.txt", "w") as f:
        f.write(context)


def read_context_from_file(channel_id, token_limit):
    with open(f"contexts/context_{channel_id}.txt", "r") as f:
        lines = f.readlines()

    context = ""
    context_tokens = 0

    for line in reversed(lines):
        tokens = tokenizer.encode(line)
        if context_tokens + len(tokens) <= token_limit:
            context = line + context
            context_tokens += len(tokens)
        else:
            break

    return context


def get_remaining_tokens(channel_id, token_limit):
    context_tokens = sum(
        len(tokenizer.encode(line)) for line in read_context_from_file(channel_id, token_limit).splitlines()
    )
    return 1600
    # return token_limit - context_tokens - 400
