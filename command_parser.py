import lark
import classes
import functions


parser = lark.Lark(open('grammar.lark').read(), parser='lalr')


class TransformerImpl(lark.Transformer):
    def __init__(self, _vars=None):
        super().__init__()
        self._vars = _vars or {}
        self.functions = functions.get_functions(self._vars)

    def start(self, items):
        return items[0]

    def command(self, items):
        args = {}
        for item in items[2:]:
            key, val = item
            args[key] = val
        return args

    def arg(self, items):
        return items[0], items[2]

    def CNAME(self, token):
        return str(token)

    def VAR(self, token):
        var = self._vars.get(str(token))
        if var is None:
            raise lark.exceptions.UnexpectedInput(f"Variable '{token}' not found")
        return var

    def var(self, token):
        return token[1]

    def ESCAPED_STRING_DOUBLE_QUOTES(self, token):
        return token[1:-1]

    def ESCAPED_STRING_SOLO_QUOTES(self, token):
        return token[1:-1]

    def TRUE(self, token):
        return True

    def FALSE(self, token):
        return False

    def NONE(self, token):
        return None

    def SIGNED_INT(self, token):
        try:
            return int(token)
        except ValueError:
            raise lark.exceptions.UnexpectedInput(f"Invalid int number: {token}")

    def SIGNED_FLOAT(self, token):
        try:
            return float(token)
        except ValueError:
            raise lark.exceptions.UnexpectedInput(f"Invalid float number: {token}")

    def COMMAND_ARGUMENT(self, token):
        return token

    def add(self, items):
        return items[0] + items[1]

    def sub(self, items):
        return items[0] - items[1]

    def mul(self, items):
        return items[0] * items[1]

    def pow(self, items):
        return items[0] ** items[1]

    def log(self, items):
        if items[0] <= 0 or items[1] <= 0:
            raise ValueError("Logarithm base and value must be greater than zero")
        return items[1] ** (1 / items[0])

    def div(self, items):
        if items[1] == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return items[0] / items[1]

    def mod(self, items):
        if items[1] == 0:
            raise ZeroDivisionError("Modulo by zero is not allowed")
        return items[0] % items[1]

    def eq(self, items):
        return items[0] == items[1]

    def not_eq(self, items):
        return items[0] != items[1]

    def less_than(self, items):
        return items[0] < items[1]

    def less_than_or_eq(self, items):
        return items[0] <= items[1]

    def greater_than(self, items):
        return items[0] > items[1]

    def greater_than_or_eq(self, items):
        return items[0] >= items[1]

    def and_op(self, items):
        return all(items)

    def or_op(self, items):
        return any(items)

    def not_op(self, items):
        return not items[0]

    def in_op(self, items):
        if not isinstance(items[1], (list, set, dict)):
            raise lark.exceptions.UnexpectedInput(f"Second operand must be a list, set, or dict: {items[1]}")
        return items[0] in items[1]

    def not_in_op(self, items):
        if not isinstance(items[1], (list, set, dict)):
            raise lark.exceptions.UnexpectedInput(f"Second operand must be a list, set, or dict: {items[1]}")
        return items[0] not in items[1]

    def is_op(self, items):
        return items[0] is items[1]

    def is_not_op(self, items):
        return items[0] is not items[1]

    def if_else(self, items):
        return items[0] if items[1] else items[2]

    def ternary(self, items):
        return items[0] if items[1] else items[2]

    def func_call(self, items):
        name = items[1]
        items = [item for item in items if not (isinstance(item, lark.Token) and item.type in ['FUNCTION_PREFIX', 'FUNCTION', 'OPEN', 'CLOSE'])][0]
        fn = None
        for aliases, f in self.functions.items():
            if name in aliases:
                fn = f
                break
        if type(fn) is not classes.Function:
            raise lark.exceptions.UnexpectedInput(f'Function \'{name}\' not found')
        if type(items) is list:
            items: list
            return fn.function(*items) if items else fn.function()
        elif type(items) is dict:
            items: dict
            return fn.function(**items) if items else fn.function()
        else:
            raise lark.exceptions.UnexpectedInput(f'Invalid function call: {name}({items})')

    def arg_list(self, items):
        return [item for item in items if not (isinstance(item, lark.Token) and item.type == 'SEP')]

    def kwarg_list(self, items):
        return (lambda x: dict(zip(x[::2], x[1::2])))([item for item in items if not (isinstance(item, lark.Token) and item.type in ['SEP', 'EQ_ARG_FUNC'])])


def parse_command(text: str, _vars=None):
    tree = parser.parse(text)
    return TransformerImpl(_vars).transform(tree)
