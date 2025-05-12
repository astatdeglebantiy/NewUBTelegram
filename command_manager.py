import pyrogram
import config
import command_parser
import manager
import status

main_config = config.load_main_config()
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


def register_handlers(client: pyrogram.Client, _manager: manager.Manager):
    async def is_in_whitelist(_, __, message) -> bool:
        if getattr(message, 'from_user'):
            if getattr(message.from_user, 'id'):
                if str(message.from_user.id) in config.load_whitelist():
                    return True
        return False

    is_in_whitelist_filter = pyrogram.filters.create(is_in_whitelist, 'is_in_whitelist')


    async def send_files_command(_, message: pyrogram.types.Message):
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
                media = [
                    pyrogram.types.InputMediaDocument(media=path, caption=caption)
                    for caption, path in files.items()
                ]
                await client.send_media_group(message.chat.id, media)
            else:
                await client.send_message(message.chat.id, 'No "files" provided')
        except Exception as e:
            await client.send_message(message.chat.id, f'```\n{str(e)}```')

    async def send_photos_command(_, message: pyrogram.types.Message):
        try:
            try:
                parsed = command_parser.parse_command(message.text, {
                    '__client__': client,
                    '__message__': message,
                })
            except Exception as e:
                await client.send_message(message.chat.id, f'```\n{str(e)}```')
                return
            photos = parsed.get('photos', None)
            if photos:
                me = await client.get_me()
                if message.from_user and message.from_user.id == me.id:
                    await message.delete()
                media = [
                    pyrogram.types.InputMediaPhoto(media=path, caption=caption)
                    for caption, path in photos.items()
                ]
                await client.send_media_group(message.chat.id, media)
            else:
                await client.send_message(message.chat.id, 'No "photos" provided')
        except Exception as e:
            await client.send_message(message.chat.id, f'```\n{str(e)}```')

    async def send_videos_command(_, message: pyrogram.types.Message):
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
                me = await client.get_me()
                if message.from_user and message.from_user.id == me.id:
                    await message.delete()
                media = [
                    pyrogram.types.InputMediaVideo(media=path, caption=caption)
                    for caption, path in videos.items()
                ]
                await client.send_media_group(message.chat.id, media)
            else:
                await client.send_message(message.chat.id, 'No "videos" provided')
        except Exception as e:
            await client.send_message(message.chat.id, f'```\n{str(e)}```')

    async def send_command(_, message: pyrogram.types.Message):
        try:
            try:
                parsed = command_parser.parse_command(message.text, {
                    '__client__': client,
                    '__message__': message,
                })
            except Exception as e:
                await client.send_message(message.chat.id, f'```\n{str(e)}```')
                return
            text = parsed.get('text', None)
            if text:
                me = await client.get_me()
                if message.from_user and message.from_user.id == me.id:
                    await message.delete()
                await client.send_message(message.chat.id, str(text))
            else:
                await client.send_message(message.chat.id, 'No "text" provided')
        except Exception as e:
            await client.send_message(message.chat.id, f'```\n{str(e)}```')

    async def white_command(_, message: pyrogram.types.Message):
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
        if str(_id) in whitelist:
            await message.reply('That user already been in whitelist')
            return
        whitelist.append(str(_id))
        config.save_whitelist(whitelist)
        await message.reply('Complete!')

    async def black_command(_, message: pyrogram.types.Message):
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

    async def get_id_command(_, message: pyrogram.types.Message):
        try:
            parsed = command_parser.parse_command(message.text, {
                '__client__': client,
                '__message__': message,
            })
        except Exception as e:
            await client.send_message(message.chat.id, f'```\n{str(e)}```')
            return
        if replied_message := getattr(message, 'reply_to_message'):
            await message.reply(replied_message.from_user.id)
            return
        if message.chat.type == pyrogram.enums.ChatType.PRIVATE:
            await message.reply(str(message.chat.id))
            return
        await message.reply('No information provided')

    async def status_command(_, message: pyrogram.types.Message):
        return await status.status_command(_, message)

    async def stop_command(_, message: pyrogram.types.Message):
        await message.reply('Au revoir!')
        exit(0)

    async def none_command(_, message: pyrogram.types.Message):
        try:
            command_parser.parse_command(message.text, {
                '__client__': client,
                '__message__': message,
            })
        except Exception as e:
            await client.send_message(message.chat.id, f'```\n{str(e)}```')
            return


    _manager.register_handler(send_files_command.__name__, send_files_command, (pyrogram.filters.command(commands='send_files', prefixes=DEFAULT_COMMAND_PREFIX) & (
            pyrogram.filters.me | is_in_whitelist_filter)))
    _manager.register_handler(send_photos_command.__name__, send_photos_command, (pyrogram.filters.command(commands='send_photos', prefixes=DEFAULT_COMMAND_PREFIX) & (
            pyrogram.filters.me | is_in_whitelist_filter)))
    _manager.register_handler(send_videos_command.__name__, send_videos_command, (pyrogram.filters.command(commands='send_videos', prefixes=DEFAULT_COMMAND_PREFIX) & (
            pyrogram.filters.me | pyrogram.filters.create(is_in_whitelist))))
    _manager.register_handler(send_command.__name__, send_command, (pyrogram.filters.command(commands='send', prefixes=DEFAULT_COMMAND_PREFIX) & (
            pyrogram.filters.me | pyrogram.filters.create(is_in_whitelist))))
    _manager.register_handler(white_command.__name__, white_command, (pyrogram.filters.command(commands='white', prefixes=DEFAULT_COMMAND_PREFIX) & pyrogram.filters.me))
    _manager.register_handler(black_command.__name__, black_command, (pyrogram.filters.command(commands='black', prefixes=DEFAULT_COMMAND_PREFIX) & pyrogram.filters.me))
    _manager.register_handler(get_id_command.__name__, get_id_command, (pyrogram.filters.command(commands='get_id', prefixes=DEFAULT_COMMAND_PREFIX) & (
            pyrogram.filters.me | pyrogram.filters.create(is_in_whitelist))))
    _manager.register_handler(status_command.__name__, status_command, (pyrogram.filters.command(commands=f'status-{client.name}', prefixes=DEFAULT_COMMAND_PREFIX) & (
            pyrogram.filters.me | pyrogram.filters.create(is_in_whitelist))))
    _manager.register_handler(stop_command.__name__, stop_command, (pyrogram.filters.command(commands='stop', prefixes=DEFAULT_COMMAND_PREFIX) & pyrogram.filters.me))
    _manager.register_handler(none_command.__name__, none_command, (pyrogram.filters.command(commands='none', prefixes=DEFAULT_COMMAND_PREFIX) & (
            pyrogram.filters.me | pyrogram.filters.create(is_in_whitelist))))
