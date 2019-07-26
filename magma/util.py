import magma as m


def BitOrBits(width):
    if width is None:
        return m.Bit
    if not isinstance(width, int):
        raise ValueError(f"Expected width to be None or int, got {width}")
    return m.Bits[width]


def pretty_str(t):
    if isinstance(t, m.TupleKind):
        args = []
        for i in range(t.N):
            key_str = str(t.Ks[i])
            val_str = pretty_str(t.Ts[i])
            indent = " " * 4
            val_str = f"\n{indent}".join(val_str.splitlines())
            args.append(f"{key_str} = {val_str}")
        # Pretty print by using newlines + indent
        joiner = ",\n    "
        result = joiner.join(args)
        # Insert first newline + indent and last newline
        result = "\n    " + result + "\n"
        s = f"Tuple({result})"
    elif isinstance(t, m.BitsKind):
        s = str(t)
    elif isinstance(t, m.ArrayKind):
        s = f"Array[{t.N}, {pretty_str(t.T)}]"
    else:
        s = str(t)
    return s


def pretty_print_type(t):
    print(pretty_str(t))
