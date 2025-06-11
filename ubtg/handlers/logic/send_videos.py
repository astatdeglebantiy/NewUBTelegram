import pyrogram
from ubtg import config, command_parser
from ubtg.handlers import filters

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
        videos = parsed.get('videos', None)
        if videos:
            media = [
                pyrogram.types.InputMediaVideo(media=path, caption=caption)
                for caption, path in videos.items()
            ]
            await client.send_media_group(message.chat.id, media)
        else:
            await client.send_message(message.chat.id, 'No "videos" provided')
    except Exception as e:
        await client.send_message(message.chat.id, f'```\n{str(e)}```')

handler_filter = pyrogram.filters.command(commands=['send_videos', 'sv'], prefixes=DEFAULT_COMMAND_PREFIX) & (pyrogram.filters.me | filters.is_in_whitelist)