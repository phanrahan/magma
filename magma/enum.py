import magma as m

def Enum(**kwargs):
    max_value = max(value for value in kwargs.values())
    num_bits = max(max_value.bit_length(), 1)
    type_ = m.Bits(num_bits)
    for key, value in kwargs.items():
        setattr(type_, key, m.bits(value, num_bits))
    return type_
