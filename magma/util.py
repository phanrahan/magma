import magma as m


def BitOrBits(width):
    if width is None:
        return m.Bit
    if not isinstance(width, int):
        raise ValueError(f"Expected width to be None or int, got {width}")
    return m.Bits[width]
