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
        command_name = items[1]
        args = {}
        for item in items[2:]:
            key, val = item
            args[key] = val
        return {'__command__': command_name, **args}

    def arg(self, items):
        return items[0], items[1]

    def CNAME(self, token):
        return str(token)

    def ESCAPED_STRING(self, token):
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
