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
        message_info = {
            'chat_id': parsed.get('chat_id', message.chat.id),
            'text': parsed.get('text', None),
            'parse_mode': parsed.get('parse_mode', None),
            'entities': parsed.get('entities', None),
            'disable_web_page_preview': parsed.get('disable_web_page_preview', None),
            'disable_notification': parsed.get('disable_notification', None),
            'reply_to_message_id': parsed.get('reply_to_message_id', None),
            'schedule_date': parsed.get('schedule_date', None),
            'protect_content': parsed.get('protect_content', None),
            'reply_markup': parsed.get('reply_markup', None)
        }
        await client.send_message(**message_info)
    except Exception as e:
        await client.send_message(message.chat.id, f'```\n{str(e)}```')


handler_filter = pyrogram.filters.command(commands=['send', 's'], prefixes=DEFAULT_COMMAND_PREFIX) & (pyrogram.filters.me | filters.is_in_whitelist)
