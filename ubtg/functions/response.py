class Response:
    def __init__(self, value, _vars=None):
        if _vars is None:
            _vars = {}
        self.value = value
        self._vars = _vars
