import importlib
import sys
from importlib import util
from pathlib import PurePath
from ubtg import classes, config


def get_function_by_name(function_name: str) -> classes.Function | None:
    print(f'Importing function "{function_name}"...')
    functions_yaml: dict = config.load_yaml(config.FUNCTIONS_YAML_PATH)
    info: dict = functions_yaml.get(function_name)
    if not info:
        raise ValueError(f'Function not found in YAML file: {function_name}')
    if not info.get('logic') and not info.get('eval_logic'):
        print(f'Function "{function_name}" does not have a "logic" or "eval_logic" key in the YAML file.\n')
        raise ValueError(f'Function "{function_name}" does not have a "function" key in the YAML file.')
    if _function := info.get('eval_logic'):
        ret = classes.Function(info.get('full_name', function_name), info.get('description', 'No description yet'), eval(_function), info.get('param_description', None))
        print(f'Successfully imported function:    {ret.full_name} - {ret.description}\n')
        return ret
    else:
        logic = info.get('logic')
        try:
            module_name = PurePath(logic).stem
            spec = importlib.util.spec_from_file_location(module_name, logic)
            logic_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logic_module)
            sys.modules[module_name] = logic_module
            _function = getattr(logic_module, '_function')
            if not callable(_function):
                raise ValueError(f'Function "{function_name}" is not callable.')
            ret = classes.Function(
                full_name=info.get('full_name') or function_name,
                description=info.get('description') or 'No description yet',
                function=_function,
                need_vars=info.get('need_vars') or False,
                param_description=info.get('param_description')
            )
            print(f'Successfully imported function:    {ret.full_name} ({function_name}) - {ret.description}\n')
            return ret
        except Exception as e:
            print(f'Error importing function {function_name}: {e}\n')
            raise ValueError(f'Error importing function {function_name}: {e}')
