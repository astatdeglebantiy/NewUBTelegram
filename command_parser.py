import dill
import subprocess
from collections.abc import Callable
import matplotlib
import config
import matplotlib.pyplot as plt
import ai_gemini

main_config = config.load_main_config()

matplotlib.use('Agg')


def shell(cmd: str):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }


def latex(
        text: str,
        font_size: int = 30,
        transparent: bool = False,
        dpi: int = 300,
        output_path: str = f'{config.TEMP_PATH}latex.png'
) -> str:
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, text, fontsize=font_size, ha='center', va='center')
    ax.axis('off')
    plt.savefig(output_path, dpi=dpi, transparent=transparent, )
    plt.close()
    return output_path


def get_functions_guide(functions: dict) -> str:
    builtin_functions_description = {
        'int': 'Just calling "int" function, like int(arg1, arg2, ... argn)',
        'float': 'Just calling "float" function, like float(arg1, arg2, ... argn)',
    }
    guide = ''
    for name, func in functions.items():
        if name not in builtin_functions_description.keys():
            try:
                source = dill.source.getsource(func)
            except Exception:
                source = f'{func} {type(func)}'
            guide += f"{name}:\n{source.strip()}\n\n"
        else:
            guide += f"{name}:\n{builtin_functions_description[name]}\n\n"
    return f'```\n{guide.strip()}```'


def fast_gemini(args):
    _dict = dict(zip(args[::2], args[1::2]))
    if not _dict:
        return f'Dict is empty'
    text = ''
    prompt = _dict.get("prompt")
    prompt_length = _dict.pop("prompt_length") if _dict.get("prompt_length") else 50
    if prompt:
        short_prompt = (prompt[:prompt_length-3] + '...') if len(prompt) > prompt_length else prompt
        text += f'**Prompt:**\n```ᅠ ᅠ \n{short_prompt}\nᅠ ᅠ ```\n\n'
    text += f'**Media:**\n```ᅠ ᅠ \n{_dict.get("media")}\nᅠ ᅠ ```\n\n' if _dict.get("media") else ''
    text += f'**Sys prompt:**\n```ᅠ ᅠ \n{_dict.get("system_prompt")}\nᅠ ᅠ ```\n\n' if _dict.get("system_prompt") else ''
    text += f'**Answer:**\n{ai_gemini.generate_content(**_dict).text}'
    return text


def set_var(_vars: dict, var_name, var=None):
    if (not str(var_name).startswith('__')) and (not str(var_name).endswith('__')):
        _vars[str(var_name)] = var


def parse_command(text: str, _vars: dict | None = None):
    if not _vars:
        _vars = {}
    default_function_prefix = main_config['DEFAULT_FUNCTION_PREFIX']
    default_prefix = main_config['DEFAULT_COMMAND_PREFIX']
    text_dict = {}
    text_list = text.split()
    prefix = text_list[0][0]
    if not prefix == default_prefix:
        raise ValueError(f'Invalid syntax: Prefix must be "{default_prefix}"')
    command = text_list[0][1:]
    command_with_prefix = text_list[0]
    for i in range(1, len(text_list)):
        argument = text_list[i]
        key_and_value = argument.split('=')
        if not len(key_and_value) == 2:
            raise ValueError('Invalid syntax: Only one equality symbol allowed in arguments')
        key, value = key_and_value
        if key.startswith('__') and key.endswith('__'):
            raise ValueError('Invalid syntax: No system arguments allowed')
        if value.startswith(default_function_prefix):
            text_dict[key] = parse_function(value, _vars)
        else:
            text_dict[key] = value
    text_dict['__prefix__'] = prefix
    text_dict['__command__'] = command
    text_dict['__command_with_prefix__'] = command_with_prefix
    return text_dict


def parse_function(_text: str, _vars: dict | None = None):
    functions: dict[str, Callable] = {
        'call': lambda x, *args: x(*args),
        'call_dict': lambda x, args: x(**args),
        'dict': lambda *args: dict(zip(args[::2], args[1::2])),
        'e': lambda *_: '\n',
        'ebrckt': lambda *_: ')',
        'enter': lambda *_: '\n',
        'eq': lambda *args: all(arg == args[0] for arg in args),
        'eqsymb': lambda *_: '=',
        'eval': lambda text: eval(text),
        'exec': lambda text: exec(text),
        'ESstr': lambda *args: ' '.join(
            str(arg).replace('\\n', '\n') for arg in args
        ),
        'Estr': lambda *args: ''.join(
            '\n' if arg == '\\n' else str(arg) for arg in args
        ),
        'fastgem': lambda *args: fast_gemini(args),
        'float': float,
        'gemgen': lambda args: ai_gemini.generate_content(**args),
        'get': lambda obj, key: obj.get(key),
        'getattr': lambda obj, key, default=None: (
            getattr(obj, key) if getattr(obj, key, None) is not None else default
        ),
        'getvar': lambda arg, default=None: _vars.get(arg, default),
        'guide': lambda *_: get_functions_guide(functions),
        'int': int,
        'latex': latex,
        'list': lambda *args: list(args),
        'loop': lambda x, n: [x() for _ in range(n)],
        'none': lambda *_: None,
        'not': lambda arg: ~arg,
        'pashalka': lambda *_: 'LJEDMITRII CUЩECTBUET',
        'rstr': lambda text: rf'{str(text)}',
        's': lambda *_: ' ',
        'sbrckt': lambda *_: '(',
        'setvar': lambda var_name, var=None: set_var(_vars, var_name, var),
        'shell': shell,
        'Sstr': lambda *args: ' '.join(str(arg) for arg in args),
        'str': lambda *args: ''.join(str(arg) for arg in args),
        'tab': lambda *_: '    ',
    }
    default_prefix = main_config['DEFAULT_FUNCTION_PREFIX']
    separator = main_config['DEFAULT_FUNCTION_SEPARATOR']
    prefix = default_prefix
    if not _text.startswith(prefix):
        raise ValueError(f'Invalid syntax: Prefix is not "{prefix}"')
    t = _text[len(prefix):]
    if '(' in t and t.endswith(')'):
        name, inner = t.split('(', 1)
        inner = inner[:-1]
        _args, buf, lvl, i = [], '', 0, 0
        while i < len(inner):
            if inner[i] == '(':
                lvl += 1; buf += inner[i]
            elif inner[i] == ')':
                lvl -= 1; buf += inner[i]
            elif inner[i:i+2] == separator and lvl == 0:
                _args.append(buf); buf = ''; i += 1
            else:
                buf += inner[i]
            i += 1
        _args.append(buf)
        parsed = []
        for a in _args:
            a = a.strip()
            if a.startswith(prefix):
                parsed.append(parse_function(a, _vars))
            else:
                parsed.append(a)
        func = functions.get(name)
        if not func:
            raise ValueError(f'Invalid syntax: No "{name}" function exists')
        return func(*parsed)

    parts = _text.split(separator)
    name = parts[0][len(prefix):]
    func = functions.get(name)
    if not func:
        raise ValueError(f'Invalid syntax: No "{name}" function exists')
    _args = []
    for p in parts[1:]:
        if p.startswith(prefix):
            _args.append(parse_function(p, _vars))
        else:
            _args.append(p)
    return func(*_args)
