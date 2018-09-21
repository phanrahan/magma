import magma as m

def Enum(**kwargs):
    num_bits = max((len(kwargs) - 1).bit_length(), 1)
    type_ = m.Bits(num_bits)
    for key, value in kwargs.items():
        setattr(type_, key, value)
    return type_
