import magma as m
from enum import Enum as pyEnum



class EnumMeta(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs, **kwargs)
        kwargs = {}
        for key, value in attrs.items():
            if key[:2] == "__":
                continue
            kwargs[key] = value
        if not kwargs:
            return cls
        max_value = max(value for value in kwargs.values())
        num_bits = max(max_value.bit_length(), 1)
        type_ = m.Bits[num_bits]
        # TODO: Make Enum a subtype of Bits instead
        type_._is_magma_enum = True
        for key, value in kwargs.items():
            setattr(type_, key, m.bits(value, num_bits))
        return type_

class Enum(metaclass=EnumMeta):
    pass


# def Enum(**kwargs):
#     max_value = max(value for value in kwargs.values())
#     num_bits = max(max_value.bit_length(), 1)
#     type_ = m.Bits[num_bits]
#     for key, value in kwargs.items():
#         setattr(type_, key, m.bits(value, num_bits))
#     return type_
