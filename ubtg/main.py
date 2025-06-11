import asyncio
import config
import pyrogram
import command_manager
import classes


main_config = config.load(config.MAIN_CONFIG_PATH)
API_KEYS = config.load(config.API_KEYS_PATH)

DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']

client = pyrogram.Client(
    name='user-bot',
    api_id=API_KEYS['API_ID'],
    api_hash=API_KEYS['API_HASH'],
    phone_number=API_KEYS['PHONE'],
    password=API_KEYS['CLOUD_PASSWORD']
)


_manager = classes.Manager(None)


async def dotted_message(message: pyrogram.types.Message):
    frames = [".", "..", "..."]
    i = 0
    try:
        while True:
            await message.edit(f'{message.text}{frames[i % len(frames)]}')
            i += 1
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        pass


@client.on_message(pyrogram.filters.command(commands='reload', prefixes=DEFAULT_COMMAND_PREFIX) & pyrogram.filters.me)
async def reload_command(_, message: pyrogram.types.Message):
    print('\n\nRELOADING...\n')
    new_message = await message.reply('Wait a minute')
    dotted_task = asyncio.create_task(dotted_message(new_message))
    global main_config
    try:
        # reload modules
        # not working

        # for item in [config, _status, command_manager, function_manager, command_parser]:
        #     module_name = PurePath(item.__file__).stem
        #     spec = importlib.util.spec_from_file_location(module_name, item.__file__)
        #     module = importlib.util.module_from_spec(spec)
        #     spec.loader.exec_module(module)
        #     sys.modules[module_name] = module
        main_config = config.load(config.MAIN_CONFIG_PATH)
        if _manager:
            _manager.clear_handlers()
            command_manager.register_handlers(client, _manager)
            print(_manager.list_handlers())
    except Exception as e:
        if dotted_task:
            dotted_task.cancel()
            try:
                await dotted_task
            except asyncio.CancelledError:
                pass
            print(f'\nRELOAD ERROR: {e}\n\n')
            await new_message.edit(f'**Reload stopped with error:**```\n{e}```')
            return
    if dotted_task:
        dotted_task.cancel()
        try:
            await dotted_task
        except asyncio.CancelledError:
            pass
    print('\nRELOAD COMPLETE!\n\n')
    await new_message.edit('**Reload complete!**')


async def main():
    global _manager
    await client.start()
    config.clear_temp()
    _manager = classes.Manager(client)
    command_manager.register_handlers(client, _manager)
    print(_manager.list_handlers())
    print('\nUSERBOT STARTED!\n\n')
    await pyrogram.idle()

client.run(main())
