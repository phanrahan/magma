import dataclasses as dc
from hwtypes.adt_meta import ProductMeta
import magma as m
from collections import OrderedDict


class MagmaProductMeta(ProductMeta):
    @classmethod
    def _from_fields(mcs, fields, name, bases, ns, cache, **kwargs):
        assert fields
        return m.Tuple(**fields)


class Product(metaclass=MagmaProductMeta):
    pass
