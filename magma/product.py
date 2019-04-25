import dataclasses as dc
from hwtypes.adt_meta import ProductMeta
import magma as m
from collections import OrderedDict


class MagmaProductMeta(ProductMeta):
    @classmethod
    def from_fields(mcs, fields, name, bases, ns, **kwargs):
        assert fields
        return m.Tuple(**fields)


class Product(metaclass=MagmaProductMeta):
    pass
