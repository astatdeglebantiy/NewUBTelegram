import pyrogram
from ubtg import config, command_parser
from ubtg.handlers import filters

main_config = config.load(config.MAIN_CONFIG_PATH)
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


async def handler(_, message: pyrogram.types.Message):
    try:
        try:
            parsed = command_parser.parse_command(message.text, {
                '__client__': _,
                '__message__': message,
            })
        except Exception as e:
            await _.send_message(message.chat.id, f'```\n{str(e)}```')
            return
        photos = parsed.get('photos', None)
        if photos:
            me = await _.get_me()
            if message.from_user and message.from_user.id == me.id:
                await message.delete()
            media = [
                pyrogram.types.InputMediaPhoto(media=path, caption=caption)
                for caption, path in photos.items()
            ]
            await _.send_media_group(message.chat.id, media)
        else:
            await _.send_message(message.chat.id, 'No "photos" provided')
    except Exception as e:
        await _.send_message(message.chat.id, f'```\n{str(e)}```')

handler_filter = pyrogram.filters.command(commands=['send_photos', 'sp'], prefixes=DEFAULT_COMMAND_PREFIX) & (pyrogram.filters.me | filters.is_in_whitelist)
