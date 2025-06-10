import pyrogram
import config


async def is_in_whitelist(_, __, message) -> bool:
    if getattr(message, 'from_user'):
        if getattr(message.from_user, 'id'):
            if str(message.from_user.id) in config.load_whitelist():
                return True
    return False


is_in_whitelist = pyrogram.filters.create(is_in_whitelist, 'is_in_whitelist')