import subprocess
import matplotlib
import classes
import config
import matplotlib.pyplot as plt
import ai_gemini

main_config = config.load(config.MAIN_CONFIG_PATH)

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
    plt.savefig(output_path, dpi=dpi, transparent=transparent)
    plt.close()
    return output_path


def get_functions(_vars: dict | None) -> dict[tuple[str, ...], classes.Function]:
    functions = {
        ('abs',): classes.Function(
            full_name='Absolute',
            description='A built-in function `abs` in Python.',
            _callable=abs
        ),
        ('call',): classes.Function(
            full_name='Call function',
            description='It just a function call.\n'
                        ':param x: The object that is being called.\n'
                        ':return: The result of the called function.',
            _callable=lambda x, arg: x(arg)
        ),
        ('callArgs',): classes.Function(
            full_name='Calling a function with a list of arguments',
            description='Calling a function with a list of arguments (i.e. with further unpacking via *).\n'
                        ':param x: The object that is being called.\n'
                        ':param args: Arguments to the function that will be unpacked via "*".\n'
                        ':return: The result of the called function.',
            _callable=lambda x, args: x(*args)
        ),
        ('callKw',): classes.Function(
            full_name='Calling a function with a dictionary of arguments',
            description='Calling a function with a dictionary of arguments (i.e. with further unpacking via **).\n'
                        ':param x: The object that is being called.\n'
                        ':param kwargs: Arguments to the function that will be unpacked via "**".\n'
                        ':return: The result of the called function.',
            _callable=lambda x, kwargs: x(**kwargs)
        ),
        ('dict',): classes.Function(
            full_name='Dictionary',
            description='A built-in function dict in Python.',
            _callable=dict
        ),
        ('e','enter'): classes.Function(
            full_name='Enter symbol',
            description='It just returns nl (`\\n`).\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: nl.',
            _callable=lambda *_: '\n'
        ),
        ('eb','ebrckt'): classes.Function(
            full_name='Enter bracket',
            description='It just returns ).\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: `)`.',
            _callable=lambda *_: ')'
        ),
        ('eq','eqsymb'): classes.Function(
            full_name='Equality symbol',
            description='It just returns =.\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: `=`.',
            _callable=lambda *_: '=',
        ),
        ('ESsStr','SEsStr'): classes.Function(
            full_name='Enter/Space-Separated Space-Separated/Enter Simple string',
            description='Converts arguments to strings, replaces literal nl (`\\n`) with actual nl, and joins them with spaces.\n'
                        ':param args: Texts for general text.\n'
                        ':return: Result of text processing.',
            _callable=lambda *args: ' '.join(str(arg).replace('\\n', '\n') for arg in args)
        ),
        ('EsStr',): classes.Function(
            full_name='Enter Simple string',
            description='Converts arguments to strings, replaces literal nl (`\\n`) with an actual nl, and joins them without spaces.\n'
                        ':param args: Texts for general text.\n'
                        ':return: Result of text processing.',
            _callable=lambda *args: ''.join('\n' if arg == '\\n' else str(arg) for arg in args)
        ),
        ('eval',): classes.Function(
            full_name='Evaluate',
            description='A built-in function `eval` in Python, but only accepts text as an argument.\n'
                        ':param text: Text for evaluating.',
            _callable=lambda text: eval(text)
        ),
        ('exec',): classes.Function(
            full_name='Execute',
            description='A built-in function `exec` in Python, but only accepts text as an argument.\n'
                        ':param text: Text for executing.',
            _callable=lambda text: exec(text)
        ),
        ('fastgem',): classes.Function(
            full_name='Fast Gemini',
            description='Quickly and conveniently receiving text from Gemini AI.\n'
                        ':param kwargs: __Check project github (__ `github` __function).__\n'
                        ':return: Received text.',
            _callable=lambda kwargs: fast_gemini(kwargs)
        ),
        ('float',): classes.Function(
            full_name='Floating point number',
            description='A built-in function float in Python.',
            _callable=float
        ),
        ('funcguide',): classes.Function(
            full_name='Function guide',
            description=':param function: Function in functions.\n'
                        ':return: Function guide.\n',
            _callable=lambda function: get_function_guide(functions, function)
        ),
        ('gemgen',): classes.Function(
            full_name='Gemini AI content generation',
            description='Gemini AI content generation.\n'
                        ':param kwargs: __Check project github (__ `github` __function).__\n'
                        ':return: Generated content.',
            _callable=lambda **kwargs: ai_gemini.generate_content(**kwargs)
        ),
        ('get',): classes.Function(
            full_name='Get item by key from dictionary',
            description='Get item by key from dictionary (this code is as simple as ever).\n'
                        ':param obj: The object from which the item must be got.\n'
                        ':param key: The key that needs to be provided to the dictionary.\n'
                        ':return: Item from dictionary.',
            _callable=lambda obj, key: obj.get(key)
        ),
        ('getattr',): classes.Function(
            full_name='Get attribute from object',
            description='A built-in function getattr in Python.',
            _callable=getattr
        ),
        ('getvar',): classes.Function(
            full_name='Get variable',
            description='Get variable from command parsers variables.\n'
                        ':param key: Variable key.\n'
                        ':return: Variable data.',
            _callable=lambda key: _vars.get(key)
        ),
        ('github',): classes.Function(
            full_name='Project GitHub',
            description='GitHub of this holy greatest project.\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: GitHub link.',
            _callable=lambda *_: 'https://github.com/astatdeglebantiy/NewUBTelegram'
        ),
        ('guide',): classes.Function(
            full_name='Functions guide',
            description=':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: Functions guide.',
            _callable=lambda *_: get_functions_guide(functions),
        ),
        ('int',): classes.Function(
            full_name='Integer',
            description='A built-in function int in Python.',
            _callable=int
        ),
        ('latex',): classes.Function(
            full_name='LaTeX image generation',
            description='__Check params on github (__ `github` __function).__\n'
                        ':return: Image path.',
            _callable=latex
        ),
        ('list',): classes.Function(
            full_name='Make the list object',
            description='Creates a list from the provided arguments.',
            _callable=lambda *args: list(args)
        ),
        ('loop',): classes.Function(
            full_name='Loop Execution',
            description='Executes a callable x for n times and returns a list of results.\n'
                        ':param x: Callable to execute.\n'
                        ':param n: Number of times to execute.\n'
                        ':return: List of results from x().',
            _callable=lambda x, n: [x() for _ in range(n)]
        ),
        ('none',): classes.Function(
            full_name='None Value',
            description='Returns None. Ignores any arguments.',
            _callable=lambda *_: None
        ),
        ('not',): classes.Function(
            full_name='Bitwise Not',
            description='Performs a bitwise NOT operation (~) on the argument.\n'
                        ':param arg: The value to operate on.\n'
                        ':return: Result of ~arg.',
            _callable=lambda arg: ~arg
        ),
        ('pashalka',): classes.Function(
            full_name='Pashalka Easter Egg',
            description='Returns a specific string. Ignores any arguments.',
            _callable=lambda *_: 'LJEDMITRII CUЩECTBUET'
        ),
        ('raw',): classes.Function(
            full_name='Raw String Representation',
            description='Returns the raw string representation of the input (rf\'...\').\n'
                        ':param text: The text to convert.\n'
                        ':return: Raw string representation.',
            _callable=lambda text: rf'{str(text)}'
        ),
        ('s',): classes.Function(
            full_name='Space Character',
            description='Returns a single space character. Ignores any arguments.',
            _callable=lambda *_: ' '
        ),
        ('sb','sbrckt',): classes.Function(
            full_name='Opening Parenthesis Character',
            description='Returns an opening parenthesis `(`. Ignores any arguments.',
            _callable=lambda *_: '('
        ),
        ('sdict',): classes.Function(
            full_name='Simple Dictionary from Arguments',
            description='Creates a dictionary from a sequence of arguments (key1, value1, key2, value2, ...).\n'
                        ':param args: Alternating keys and values.\n'
                        ':return: A new dictionary.',
            _callable=lambda *args: dict(zip(args[::2], args[1::2]))
        ),
        ('setvar',): classes.Function(
            full_name='Set Variable in Scope',
            description='Sets a variable in the _vars dictionary.\n'
                        ':param var_name: The name of the variable (string).\n'
                        ':param var: The value to assign to the variable (defaults to None).\n'
                        ':return: None.',
            _callable=lambda var_name, var=None: set_var(_vars, var_name, var)
        ),
        ('shell',): classes.Function(
            full_name='Execute Shell Command',
            description='Executes a shell command and returns a dictionary with stdout, stderr, and returncode.\n'
                        ':param cmd: The command string to execute.\n'
                        ':return: Dictionary containing execution results.',
            _callable=shell
        ),
        ('Ssstr',): classes.Function(
            full_name='Space-Separated String Concatenation',
            description='Converts all arguments to strings and joins them with spaces.\n'
                        ':param args: Objects to convert to string and join.\n'
                        ':return: A single string.',
            _callable=lambda *args: ' '.join(str(arg) for arg in args)
        ),
        ('sstr',): classes.Function(
            full_name='Simple String Concatenation',
            description='Converts all arguments to strings and concatenates them without spaces.\n'
                        ':param args: Objects to convert to string and join.\n'
                        ':return: A single string.',
            _callable=lambda *args: ''.join(str(arg) for arg in args)
        ),
        ('str',): classes.Function(
            full_name='String Conversion',
            description='A built-in function str in Python. Converts an object to its string representation.',
            _callable=str
        ),
        ('tab',): classes.Function(
            full_name='Tab Character',
            description='Returns a tab character (4 spaces). Ignores any arguments.',
            _callable=lambda *_: '    '
        ),
        ('uniform',): classes.Function(
            full_name='Check Uniformity of Arguments',
            description='Checks if all provided arguments are equal to the first argument.\n'
                        'Returns True if no arguments are provided or if all arguments are equal.\n'
                        ':param args: Arguments to compare.\n'
                        ':return: Boolean indicating uniformity.',
            _callable=lambda *args: all(arg == args[0] for arg in args) if args else True
        ),
        ('XEY',): classes.Function(
            full_name='X Equals Y (Equality)',
            description='Checks if x is equal to y (x == y).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x == y.',
            _callable=lambda x, y: x == y
        ),
        ('XGTY',): classes.Function(
            full_name='X Greater Than Y',
            description='Checks if x is greater than y (x > y).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x > y.',
            _callable=lambda x, y: x > y
        ),
        ('XIY',): classes.Function(
            full_name='X Is Y (Identity)',
            description='Checks if x is the same object as y (x is y).\n'
                        ':param x: First object.\n'
                        ':param y: Second object.\n'
                        ':return: Boolean result of x is y.',
            _callable=lambda x, y: x is y
        ),
        ('XLTY',): classes.Function(
            full_name='X Less Than Y',
            description='Checks if x is less than y (x < y).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x < y.',
            _callable=lambda x, y: x < y
        ),
        ('XNEY',): classes.Function(
            full_name='X Not Equals Y (Inequality)',
            description='Checks if x is not equal to y (x != y).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x != y.',
            _callable=lambda x, y: x != y
        ),
    }
    return functions


def get_function_guide(functions: dict[tuple[str, ...], classes.Function], function_name) -> str:
    for aliases, function in functions.items():
        if function_name in aliases:
            return f'**{function.full_name}** `{aliases}`:\n{function.description}'
    raise ValueError(f'No function named "{function_name}"')


def get_functions_guide(functions: dict[tuple[str, ...], classes.Function]) -> str:
    text = ''
    for aliases, function in functions.items():
        text += f'**{function.full_name}** `{aliases}`:\n{function.description}\n\n'
    return text


def fast_gemini(kwargs):
    _dict = dict(zip(kwargs[::2], kwargs[1::2]))
    if not _dict:
        return f'Dict is empty'
    text = ''
    prompt = _dict.get("prompt")
    prompt_length = _dict.pop("prompt_length") if _dict.get("prompt_length") else 50
    if prompt:
        short_prompt = (prompt[:int(prompt_length)-3] + '...') if len(prompt) > int(prompt_length) else prompt
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
    functions = get_functions(_vars)
    default_prefix = main_config['DEFAULT_FUNCTION_PREFIX']
    separator = main_config['DEFAULT_FUNCTION_SEPARATOR']
    if not _text.startswith(default_prefix):
        raise ValueError(f'Invalid syntax: Prefix is not "{default_prefix}"')
    t = _text[len(default_prefix):]
    if '(' in t and t.endswith(')'):
        name, inner = t.split('(', 1)
        inner = inner[:-1]
        args, buf, lvl, i = [], '', 0, 0
        while i < len(inner):
            if inner[i] == '(':
                lvl += 1; buf += inner[i]
            elif inner[i] == ')':
                lvl -= 1; buf += inner[i]
            elif inner[i:i+len(separator)] == separator and lvl == 0:
                args.append(buf.strip()); buf = ''; i += len(separator) - 1
            else:
                buf += inner[i]
            i += 1
        if buf:
            args.append(buf.strip())
        parsed_args = []
        for a in args:
            if a.startswith(default_prefix):
                parsed_args.append(parse_function(a, _vars))
            else:
                parsed_args.append(a)
    else:
        name = t
        parsed_args = []
    func_obj = None
    for aliases, fn in functions.items():
        if name in aliases:
            func_obj = fn
            break
    if func_obj is None:
        raise ValueError(f'Invalid syntax: No function named "{name}"')
    return func_obj.callable(*parsed_args)
