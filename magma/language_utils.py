_PRIMITIVE_TO_PYTHON_MAP = {
    "and": "and_",
    "or": "or_",
    "xor": "xor",
    "shl": "lshift",
    "lshr": "rshift",
    "ashr": "rshift",
    "urem": "mod",
    "srem": "mod",
    "udiv": "floordiv",
    "sdiv": "floordiv",
    "ule": "le",
    "ult": "lt",
    "uge": "ge",
    "ugt": "gt",
    "sle": "le",
    "slt": "lt",
    "sge": "ge",
    "sgt": "gt",
    "not": "invert"
}


def primitive_to_python(key):
    return _PRIMITIVE_TO_PYTHON_MAP.get(key, key)
