import subprocess
import matplotlib
from matplotlib import pyplot as plt
import ai_gemini
import classes
import config


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


def get_function_guide(functions: dict[tuple[str, ...], classes.Function], function_name) -> str:
    for aliases, function in functions.items():
        if function_name in aliases:
            return f'**{function.full_name}** `{aliases}`:\n{function.description}'
    raise ValueError(f'No function named "{function_name}"')


def get_functions_guide(functions: dict[tuple[str, ...], classes.Function], page: int = 0) -> str:
    text = ''
    for aliases, function in list(functions.items())[:10*(page+1)]:
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


def get_functions(_vars: dict | None) -> dict[tuple[str, ...], classes.Function]:
    functions = {
        ('abs',): classes.Function(
            full_name='Absolute',
            description='A built-in function `abs` in Python.',
            function=abs
        ),
        ('call',): classes.Function(
            full_name='Call function',
            description='It just a function call.\n'
                        ':param x: The object that is being called.\n'
                        ':return: The result of the called function.',
            function=lambda x, arg: x(arg)
        ),
        ('callArgs',): classes.Function(
            full_name='Calling a function with a list of arguments',
            description='Calling a function with a list of arguments (i.e. with further unpacking via *).\n'
                        ':param x: The object that is being called.\n'
                        ':param args: Arguments to the function that will be unpacked via "*".\n'
                        ':return: The result of the called function.',
            function=lambda x, args: x(*args)
        ),
        ('callKw',): classes.Function(
            full_name='Calling a function with a dictionary of arguments',
            description='Calling a function with a dictionary of arguments (i.e. with further unpacking via double-star).\n'
                        ':param x: The object that is being called.\n'
                        ':param kwargs: Arguments to the function that will be unpacked via double-star.\n'
                        ':return: The result of the called function.',
            function=lambda x, kwargs: x(**kwargs)
        ),
        ('cb', 'cbrckt', 'cprnthsis'): classes.Function(
            full_name='Closing Parenthesis',
            description='It just returns `)`.\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: `)`.',
            function=lambda *_: ')'
        ),
        ('dict',): classes.Function(
            full_name='Dictionary',
            description='A built-in function dict in Python.',
            function=dict
        ),
        ('e','enter',): classes.Function(
            full_name='Enter symbol',
            description='It just returns nl (`\\n`).\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: nl.',
            function=lambda *_: '\n'
        ),
        ('eval',): classes.Function(
            full_name='Evaluate',
            description='A built-in function `eval` in Python, but only accepts text as an argument.\n'
                        ':param text: Text for evaluating.',
            function=lambda text: eval(text)
        ),
        ('exec',): classes.Function(
            full_name='Execute',
            description='A built-in function `exec` in Python, but only accepts text as an argument.\n'
                        ':param text: Text for executing.',
            function=lambda text: exec(text)
        ),
        ('fastgem',): classes.Function(
            full_name='Fast Gemini',
            description='Quickly and conveniently receiving text from Gemini AI.\n'
                        ':param kwargs: __Check project github (__ `github` __function).__\n'
                        ':return: Received text.',
            function=lambda kwargs: fast_gemini(kwargs)
        ),
        ('float',): classes.Function(
            full_name='Floating point number',
            description='A built-in function float in Python.',
            function=float
        ),
        ('funcguide',): classes.Function(
            full_name='Function guide',
            description=':param function: Function in functions.\n'
                        ':return: Function guide.\n',
            function=lambda function: get_function_guide(functions, function)
        ),
        ('gemgen',): classes.Function(
            full_name='Gemini AI content generation',
            description='Gemini AI content generation.\n'
                        ':param kwargs: __Check project github (__ `github` __function).__\n'
                        ':return: Generated content.',
            function=lambda **kwargs: ai_gemini.generate_content(**kwargs)
        ),
        ('get',): classes.Function(
            full_name='Get item by key from dictionary',
            description='Get item by key from dictionary (this code is as simple as ever).\n'
                        ':param obj: The object from which the item must be got.\n'
                        ':param key: The key that needs to be provided to the dictionary.\n'
                        ':return: Item from dictionary.',
            function=lambda obj, key: obj.get(key)
        ),
        ('getattr',): classes.Function(
            full_name='Get attribute from object',
            description='A built-in function getattr in Python.',
            function=getattr
        ),
        ('github',): classes.Function(
            full_name='Project GitHub',
            description='GitHub of this holy greatest project.\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: GitHub link.',
            function=lambda *_: 'https://github.com/astatdeglebantiy/NewUBTelegram'
        ),
        ('guide',): classes.Function(
            full_name='Functions guide',
            description=':param page: Guide page (unfortunately, the whole guide does not fit).\n'
                        ':return: Functions guide.',
            function=lambda page: get_functions_guide(functions, page),
        ),
        ('int',): classes.Function(
            full_name='Integer',
            description='A built-in function int in Python.',
            function=int
        ),
        ('latex',): classes.Function(
            full_name='LaTeX image generation',
            description='__Check params on github (__ `github` __function).__\n'
                        ':return: Image path.',
            function=latex
        ),
        ('list',): classes.Function(
            full_name='Make the list object',
            description='Creates a list from the provided arguments.',
            function=lambda *args: list(args)
        ),
        ('loop',): classes.Function(
            full_name='Loop Execution',
            description='Executes a callable x for n times and returns a list of results.\n'
                        ':param x: Callable to execute.\n'
                        ':param n: Number of times to execute.\n'
                        ':return: List of results from x().',
            function=lambda x, n: [x() for _ in range(n)]
        ),
        ('none',): classes.Function(
            full_name='None Value',
            description='Returns None. Ignores any arguments.',
            function=lambda *_: None
        ),
        ('not',): classes.Function(
            full_name='Bitwise Not',
            description='Performs a bitwise NOT operation (~) on the argument.\n'
                        ':param arg: The value to operate on.\n'
                        ':return: Result of ~arg.',
            function=lambda arg: ~arg
        ),
        ('ob','obrckt','oprnthsis'): classes.Function(
            full_name='Opening Parenthesis',
            description='It just returns `(`.\n'
                        ':param *_: Accepts a list of nothing and does nothing with it.\n'
                        ':return: `(`.',
            function=lambda *_: '('
        ),
        ('pashalka',): classes.Function(
            full_name='Pashalka Easter Egg',
            description='Returns a specific string. Ignores any arguments.',
            function=lambda *_: 'LJEDMITRII CUЩECTBUET'
        ),
        ('raw',): classes.Function(
            full_name='Raw String Representation',
            description='Returns the raw string representation of the input (rf\'...\').\n'
                        ':param text: The text to convert.\n'
                        ':return: Raw string representation.',
            function=lambda text: rf'{str(text)}'
        ),
        ('sdict',): classes.Function(
            full_name='Simple Dictionary from Arguments',
            description='Creates a dictionary from a sequence of arguments (key1, value1, key2, value2, ...).\n'
                        ':param args: Alternating keys and values.\n'
                        ':return: A new dictionary.',
            function=lambda *args: dict(zip(args[::2], args[1::2]))
        ),
        ('setvar',): classes.Function(
            full_name='Set Variable in Scope',
            description='Sets a variable in the _vars dictionary.\n'
                        ':param var_name: The name of the variable (string).\n'
                        ':param var: The value to assign to the variable (defaults to None).\n'
                        ':return: None.',
            function=lambda var_name, var=None: set_var(_vars, var_name, var)
        ),
        ('shell',): classes.Function(
            full_name='Execute Shell Command',
            description='Executes a shell command and returns a dictionary with stdout, stderr, and returncode.\n'
                        ':param cmd: The command string to execute.\n'
                        ':return: Dictionary containing execution results.',
            function=shell
        ),
        ('str',): classes.Function(
            full_name='String',
            description='A built-in function str in Python. Converts an object to its string representation.',
            function=str
        ),
        ('tab',): classes.Function(
            full_name='Tab Character',
            description='Returns a tab character (4 spaces). Ignores any arguments.',
            function=lambda *_: '    '
        ),
        ('uniform',): classes.Function(
            full_name='Check Uniformity of Arguments',
            description='Checks if all provided arguments are equal to the first argument.\n'
                        'Returns None if no arguments are provided or if all arguments are equal.\n'
                        ':param args: Arguments to compare.\n'
                        ':return: Boolean indicating uniformity.',
            function=lambda *args: all(arg == args[0] for arg in args) if args else None
        ),
        ('XEY',): classes.Function(
            full_name='X Equals Y (Equality)',
            description='Checks if x is equal to y (`x == y`).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x == y.',
            function=lambda x, y: x == y
        ),
        ('XGTY',): classes.Function(
            full_name='X Greater Than Y',
            description='Checks if x is greater than y (`x > y`).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x > y.',
            function=lambda x, y: x > y
        ),
        ('XIY',): classes.Function(
            full_name='X Is Y (Identity)',
            description='Checks if x is the same object as y (`x is y`).\n'
                        ':param x: First object.\n'
                        ':param y: Second object.\n'
                        ':return: Boolean result of x is y.',
            function=lambda x, y: x is y
        ),
        ('XLTY',): classes.Function(
            full_name='X Less Than Y',
            description='Checks if x is less than y (`x < y`).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x < y.',
            function=lambda x, y: x < y
        ),
        ('XNEY',): classes.Function(
            full_name='X Not Equals Y (Inequality)',
            description='Checks if x is not equal to y (`x != y`).\n'
                        ':param x: First value.\n'
                        ':param y: Second value.\n'
                        ':return: Boolean result of x != y.',
            function=lambda x, y: x != y
        ),
    }
    return functions