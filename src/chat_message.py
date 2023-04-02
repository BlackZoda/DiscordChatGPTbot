from . import channel_context_manager as ccm
from .logger import get_logger
from .response import generate_response
from .utils.string_utils import split_string_list, re_clean
from requests.exceptions import RequestException


async def process_request(cmd_ctx, channel_id, content, user, bot):
    logger = get_logger(__name__)

    ccm.add_message_to_context(channel_id, str(cmd_ctx.author), content)

    logger.info(
        f"Received message from {cmd_ctx.author} in channel {cmd_ctx.channel}: {content}")

    logger.debug(f"Channel type: {cmd_ctx.channel.type}")

    token_limit = ccm.get_remaining_tokens(channel_id, 4097)

    try:
        response = await generate_response(
            content, channel_id, token_limit, user)
    except RequestException as e:
        response = "I'm sorry, but I encoutnered an error while processing your request. Please try again later."
        logger.exception("Error generating response")

    ccm.add_message_to_context(channel_id, str(bot.user), response)

    split_message = split_string_list([response])

    for msg in split_message:
        await cmd_ctx.send(re_clean(msg))
        logger.info(
            f"Sent message to {cmd_ctx.author} in channel {cmd_ctx.channel}: {content}")
