from magma.bits import BitsMeta, Bits
from hwtypes import BitVector


class EnumMeta(BitsMeta):
    def __new__(mcs, name, bases, attrs, **kwargs):
        # Force Bits repr for now
        attrs["orig_name"] = "Bits"
        cls = super().__new__(mcs, name, bases, attrs, **kwargs)
        fields = {}
        for key, value in attrs.items():
            if key[:2] == "__" or key == "_info_":
                continue
            if key == "orig_name":
                continue
            fields[key] = value
        if not fields:
            return cls
        for field in fields:
            if field == "N":
                # TODO: Make N unreserved
                raise ValueError("N is a reserved name in Enum")
        max_value = max(value for value in fields.values())
        num_bits = max(max_value.bit_length(), 1)
        type_ = cls[num_bits]
        type_._is_magma_enum = True
        type_.fields = fields
        for key, value in fields.items():
            setattr(type_, key, BitVector[num_bits](value))
        return type_


class Enum(Bits, metaclass=EnumMeta):
    pass
