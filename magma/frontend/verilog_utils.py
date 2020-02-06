import hwtypes


_SPECIFIERS = [("h", 16), ("o", 8), ("b", 2), ("d", 10)]


def int_const_str_to_int(value):
    """Parses a verilog integer constant (as a string) and returns an int"""
    # Default no specifier.
    size = 32
    base = 10
    signed = False
    if "'" in value:
        # Parse literal specifier.
        size, value = value.split("'")
        size = 32
        if size != "":
            size = int(size)
        signed = False
        if "s" in value:
            signed = True
            value = value.replace("s", "")
        for specifier, base in _SPECIFIERS:
            if specifier in value:  # remove specifier
                value = value.replace(specifier, "")
                break
        else:
            base = 10  # default base 10
    value = int(value, base)
    if signed:
        return hwtypes.SIntVector[size](value).as_uint()
    return hwtypes.UIntVector[size](value).as_uint()
