import math


def log2_ceil(x: int) -> int:
    return math.ceil(math.log(x, 2))


def log2_floor(x: int) -> int:
    return math.floor(math.log(x, 2))


def is_pow2(x: int) -> bool:
    return log2_ceil(x) == log2_floor(x)
