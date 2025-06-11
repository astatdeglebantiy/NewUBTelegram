from ubtg.functions.response import Response


def _function(_vars_, name: str, value):
    _vars_[name] = value
    return Response(value=value, _vars=_vars_)
