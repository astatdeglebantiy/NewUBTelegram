import lark
from ubtg import function_manager
from functions import response


class TransformerImpl(lark.Transformer):
    def __init__(self, _vars: dict | None=None):
        super().__init__()
        self._vars = _vars or {}

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

    def list(self, items):
        return items

    def dict(self, items):
        return dict(zip(items[::2], items[1::2]))

    def paren_expr(self, items):
        return items[0]

    def func_call(self, items):
        name = items[1]
        items = [item for item in items if not (isinstance(item, lark.Token) and item.type in ['FUNCTION_PREFIX', 'FUNCTION', 'OPEN', 'CLOSE'])][0]
        try:
            fn = function_manager.get_function_by_name(name)
        except Exception as e:
            raise lark.exceptions.UnexpectedInput(f'Error occurred: {e}')
        try:
            if type(items) is list:
                items: list
                if fn.need_vars is True:
                    ret = fn.function(self._vars, *items)
                else:
                    ret = fn.function(*items)
            elif type(items) is dict:
                items: dict
                if fn.need_vars is True:
                    ret = fn.function(self._vars, **items)
                else:
                    ret = fn.function(**items)
            elif not items:
                if fn.need_vars is True:
                    ret = fn.function(self._vars)
                else:
                    ret = fn.function()
            else:
                raise lark.exceptions.UnexpectedInput(f'Invalid function call: {name}({items})')
            if isinstance(ret, response.Response):
                self._vars = getattr(ret, '_vars', self._vars)
                return ret.value
            else:
                return ret
        except Exception as e:
            raise lark.exceptions.UnexpectedInput(f'Error occurred while calling function "{name}": {e}')

    def arg_list(self, items):
        return [item for item in items if not (isinstance(item, lark.Token) and item.type == 'SEP')]

    def kwarg_list(self, items):
        return (lambda x: dict(zip(x[::2], x[1::2])))([item for item in items if not (isinstance(item, lark.Token) and item.type in ['SEP', 'EQ_ARG_FUNC'])])


def parse_command(text: str, _vars: dict | None=None):
    parser = lark.Lark(open('grammar.lark').read(), parser='lalr')
    tree = parser.parse(text)
    parsed = TransformerImpl(_vars).transform(tree)
    print(f'Nonparsed: {text}')
    print(f'Parsed: {parsed}\n')
    return parsed
