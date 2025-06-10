import importlib
import sys
from pathlib import PurePath
import pyrogram
import config
import classes
import importlib.util

main_config = config.load(config.MAIN_CONFIG_PATH)
DEFAULT_COMMAND_PREFIX = main_config['DEFAULT_COMMAND_PREFIX']


def register_handlers(client: pyrogram.Client, _manager: classes.Manager):
    handlers: dict = config.load_yaml(config.HANDLERS_YAML_PATH)
    for handler_name, info in handlers.items():
        description = info.get('description', None)
        if description:
            print(f'Registering handler:   {handler_name} - {description}')
        else:
            print(f'Registering handler:   {handler_name}')
        logic = info.get('logic', None)
        if not logic:
            print(f'No logic for handler: {handler_name}')
            continue
        try:
            module_name = PurePath(logic).stem
            spec = importlib.util.spec_from_file_location(module_name, logic)
            logic_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logic_module)
            sys.modules[module_name] = logic_module
            logic_function = getattr(logic_module, 'handler', None)
            if not logic_function:
                print(f'No handler function in {logic_module.__name__}')
                continue
            handler_filter = getattr(logic_module, 'handler_filter', None)
            if not handler_filter:
                print(f'No filter for handler: {handler_name}')
                continue
            _manager.register_handler(handler_name, logic_function, handler_filter)
        except Exception as e:
            print(f'Error importing handler {handler_name}: {e}')
            continue
