import lark
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
        return items[0], items[1]

    def CNAME(self, token):
        return str(token)

    def FUNCTION(self, token):
        return str(token)

    def COMMAND(self, token):
        return str(token)

    def VAR(self, token):
        var = self._vars.get(str(token))
        if var is None:
            raise lark.exceptions.UnexpectedInput(f"Variable '{token}' not found")
        return var

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

    def func_call(self, items):
        name = items[1]
        arg_list = items[3] if len(items) > 3 else []
        fn = next(f.function for aliases, f in self.functions.items() if name in aliases)
        return fn(*arg_list)

    def arg_list(self, items):
        return [item for item in items if not isinstance(item, lark.Token) or item.type != 'SEP']


def parse_command(text: str, _vars=None):
    tree = parser.parse(text)
    return TransformerImpl(_vars).transform(tree)
