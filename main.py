import importlib
import config
import pyrogram
import command_manager
import manager
import command_parser

main_config = config.load_main_config()
API_KEYS = config.load_api_keys()

DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']

client = pyrogram.Client(
    name='user-bot',
    api_id=API_KEYS['API_ID'],
    api_hash=API_KEYS['API_HASH'],
    phone_number=API_KEYS['PHONE'],
    password=API_KEYS['CLOUD_PASSWORD']
)


@client.on_message(pyrogram.filters.command(commands='reload', prefixes=DEFAULT_COMMAND_PREFIX) & pyrogram.filters.me)
async def reload_command(_, message: pyrogram.types.Message):
    new_message = await message.reply('Uno momento...')
    global main_config
    importlib.reload(config)
    importlib.reload(command_manager)
    importlib.reload(command_parser)
    main_config = config.load_main_config()
    if _manager:
        _manager.clear_handlers()
        command_manager.register_handlers(client, _manager)
        print(_manager.list_handlers())
    await new_message.edit('Complete!')

_manager = None

async def main():
    global _manager
    await client.start()
    config.clear_temp()
    _manager = manager.Manager(client)
    command_manager.register_handlers(client, _manager)
    print(_manager.list_handlers())
    await pyrogram.idle()

client.run(main())
