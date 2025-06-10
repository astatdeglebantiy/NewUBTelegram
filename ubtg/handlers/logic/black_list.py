import pyrogram
from ubtg import config, command_parser

main_config = config.load(config.MAIN_CONFIG_PATH)
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


async def handler(client: pyrogram.Client, message: pyrogram.types.Message):
    whitelist = config.load_whitelist()
    try:
        parsed = command_parser.parse_command(message.text, {
            '__client__': client,
            '__message__': message,
            '__whitelist__': whitelist,
        })
    except Exception as e:
        await client.send_message(message.chat.id, f'```\n{str(e)}```')
        return
    _id = None
    if parsed.get('id', None):
        _id = parsed['id']
    elif replied_message := getattr(message, 'reply_to_message'):
        _id = replied_message.from_user.id
    elif message.chat.type == pyrogram.enums.ChatType.PRIVATE:
        _id = message.chat.id
    if not _id:
        await message.reply('No information provided')
        return
    if not str(_id) in whitelist:
        await message.reply('That user already not been in whitelist')
        return
    whitelist.remove(str(_id))
    config.save_whitelist(whitelist)
    await message.reply('Complete!')

handler_filter = pyrogram.filters.command(commands='black', prefixes=config.load(config.MAIN_CONFIG_PATH)['DEFAULT_COMMAND_PREFIX']) & pyrogram.filters.me