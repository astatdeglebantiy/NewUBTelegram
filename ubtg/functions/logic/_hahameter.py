import hahameter


def _function(text: str):
    return hahameter.get_score(text) if hahameter.is_haha(text) else 0.0