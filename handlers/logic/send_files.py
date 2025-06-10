import pyrogram
import command_parser
import config
from handlers import filters

main_config = config.load(config.MAIN_CONFIG_PATH)
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


async def handler(client: pyrogram.Client, message: pyrogram.types.Message):
    try:
        try:
            parsed = command_parser.parse_command(message.text, {
                '__client__': client,
                '__message__': message,
            })
        except Exception as e:
            await client.send_message(message.chat.id, f'```\n{str(e)}```')
            return
        files = parsed.get('files', None)
        if files:
            me = await client.get_me()
            if message.from_user and message.from_user.id == me.id:
                await message.delete()
            print(files.items())
            media = [
                pyrogram.types.InputMediaDocument(media=path, caption=caption)
                for caption, path in files.items()
            ]
            await client.send_media_group(message.chat.id, media)
        else:
            await client.send_message(message.chat.id, 'No "files" provided')
    except Exception as e:
        await client.send_message(message.chat.id, f'```\n{str(e)}```')


handler_filter = pyrogram.filters.command(commands=['send_files', 'sf'], prefixes=DEFAULT_COMMAND_PREFIX) & (pyrogram.filters.me | filters.is_in_whitelist)
