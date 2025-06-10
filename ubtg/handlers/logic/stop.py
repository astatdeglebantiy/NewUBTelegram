import pyrogram
from ubtg import config

main_config = config.load(config.MAIN_CONFIG_PATH)
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


async def handler(_, message: pyrogram.types.Message):
    await message.reply('Au revoir!')
    exit(0)

handler_filter = pyrogram.filters.command(commands='stop', prefixes=DEFAULT_COMMAND_PREFIX) & pyrogram.filters.me
