def _function(_vars_, dictionary: dict, key: str, default=None):
    return dictionary.get(key) if key in dictionary else default