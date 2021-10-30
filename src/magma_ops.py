from typing import Union

import magma as m

from magma_common import InstanceWrapper, value_or_type_to_string


def MagmaArrayGetOp(T: m.ArrayMeta, index: str):
    assert isinstance(T, m.ArrayMeta)
    T = T.undirected_t
    name = f"magma_array_get_op_{value_or_type_to_string(T)}"
    T_out = T.T
    ports = dict(I=m.In(T), O=m.Out(T_out))
    attrs = dict(T=T, index=index)
    return InstanceWrapper(name, ports, attrs)


class MagmaArraySliceOp(m.Generator2):
    def __init__(self, T: m.ArrayMeta, lo: int, hi: int):
        assert isinstance(T, m.ArrayMeta)
        T = T.undirected_t
        type_string = value_or_type_to_string(T)
        self.name = f"magma_array_slice_op_{type_string}_{lo}_{hi}"
        self.primitive = True

        T_out = T.unsized_t[hi - lo]
        self.io = m.IO(I=m.In(T), O=m.Out(T_out))

        self.T = T
        self.lo = lo
        self.hi = hi


def MagmaArrayCreateOp(T: m.ArrayMeta):
    assert isinstance(T, m.ArrayMeta)
    T = T.undirected_t
    name = f"magma_array_create_op_{value_or_type_to_string(T)}"
    ports = dict(**{f"I{i}": m.In(T.T) for i in range(T.N)})
    ports.update(dict(O=m.Out(T)))
    attrs = dict(T=T)
    return InstanceWrapper(name, ports, attrs)


def MagmaProductGetOp(T: m.ProductMeta, index: Union[int, str]):
    assert isinstance(T, m.ProductMeta)
    T = T.undirected_t
    name = f"magma_product_get_op_{value_or_type_to_string(T)}_{index}"
    T_out = T.field_dict[index]
    ports = dict(I=m.In(T), O=m.Out(T_out))
    attrs = dict(T=T, index=index)
    return InstanceWrapper(name, ports, attrs)


def MagmaProductCreateOp(T: m.ProductMeta):
    assert isinstance(T, m.ProductMeta)
    T = T.undirected_t
    name = f"magma_product_create_op_{value_or_type_to_string(T)}"
    fields = T.field_dict
    ports = dict(**{f"I{k}": m.In(t) for k, t in fields.items()})
    ports.update(dict(O=m.Out(T)))
    return InstanceWrapper(name, ports, {})


def MagmaBitConstantOp(T: m.DigitalMeta, value: bool):
    assert isinstance(T, m.DigitalMeta)
    T = T.undirected_t
    name = f"magma_bit_constant_op_{value_or_type_to_string(T)}"
    ports = dict(O=m.Out(T))
    attrs = dict(value=value)
    return InstanceWrapper(name, ports, attrs)


def MagmaBitsConstantOp(T: m.BitsMeta, value: int):
    assert isinstance(T, m.BitsMeta)
    T = T.undirected_t
    name = f"magma_bits_constant_op_{value_or_type_to_string(T)}"
    ports = dict(O=m.Out(T))
    attrs = dict(value=value)
    return InstanceWrapper(name, ports, attrs)
