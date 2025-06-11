import math


def _function(_vars_, x: float, base: float) -> float:
    if x <= 0 or base <= 0:
        raise ValueError("Both x and base must be greater than zero.")
    return math.log(x, base)