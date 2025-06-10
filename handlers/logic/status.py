import pyrogram
import _status
import config

main_config = config.load(config.MAIN_CONFIG_PATH)
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


async def handler(_, message: pyrogram.types.Message):
    return await _status.status_command(_, message)

handler_filter = pyrogram.filters.command(commands='status', prefixes=DEFAULT_COMMAND_PREFIX) & pyrogram.filters.me