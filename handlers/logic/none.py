import pyrogram
import command_parser
import config
from handlers import filters

main_config = config.load(config.MAIN_CONFIG_PATH)
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


async def handler(client: pyrogram.Client, message: pyrogram.types.Message):
    try:
        command_parser.parse_command(message.text, {
            '__client__': client,
            '__message__': message,
        })
    except Exception as e:
        await client.send_message(message.chat.id, f'```\n{str(e)}```')
        return

handler_filter = pyrogram.filters.command(commands='none', prefixes=DEFAULT_COMMAND_PREFIX) & (pyrogram.filters.me | filters.is_in_whitelist)