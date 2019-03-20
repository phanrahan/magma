import dataclasses as dc
import magma as m
from collections import OrderedDict


class ProductMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls = dc.dataclass(eq=True, frozen=True)(cls)
        fields = OrderedDict()
        for field in dc.fields(cls):
            fields[field.name] = field.type
        if not fields:
            return cls
        return m.Tuple(**fields)


class Product(metaclass=ProductMeta):
    pass
