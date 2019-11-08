import abc
import collections
import dataclasses
import functools
import operator
import magma as m
import mantle


class IO:
    def __init__(self, **kwargs):
        self.interface = {}
        for k, v in kwargs.items():
            port = v.flip()()
            self.interface[k] = type(port)
            setattr(self, k, port)

    def __repr__(self):
        return repr(self.interface)


class CircuitMeta(type):
    def __new__(metacls, name, bases, namespace):
        namespace.setdefault("name", name)
        return super().__new__(metacls, name, bases, namespace)


class Circuit(metaclass=CircuitMeta):
    pass


class Generator1Meta(abc.ABCMeta):
    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        return dataclasses.dataclass(cls)


class Generator1(metaclass=Generator1Meta):
    @abc.abstractmethod
    def generate(self):
        raise NotImplementedError()


class Generator2Meta(abc.ABCMeta):
    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        return dataclasses.dataclass(cls)


class Generator2(metaclass=Generator2Meta):
    @abc.abstractmethod
    def elaborate(self):
        raise NotImplementedError()

    def __post_init__(self):
        self.elaborate()
        if not hasattr(self, "IO"):
            raise Exception("Must set IO")


class Optional:
    def __init__(self, param, typ):
        self.param = param
        self.typ = typ


class IOTemplate:
    def __init__(self, **kwargs):
        self.ports = kwargs


class Symbolic:
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ


class CustomNamespace(collections.UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.___annotations = None

    def __setitem__(self, key, value):
        if key is "__annotations__":
            value = collections.UserDict()
            self.___annotations = value
        super().__setitem__(key, value)

    def __getitem__(self, key):
        if not self.___annotations or key not in self.___annotations:
            return super().__getitem__(key)
        return Symbolic(key, self.___annotations[key])


def elaborate_type(value, params):
    if isinstance(value, Symbolic):
        return getattr(params, value.name)
    if isinstance(value, Optional):
        option = elaborate_type(value.param, params)
        if not option:
            return None
        return elaborate_type(value.typ, params)
    # hacky...
    if isinstance(value, m.UIntKind):
        if not isinstance(value.N, Symbolic):
            return value
        N = elaborate_type(value.N, params)
        return m.UInt[N]
    if isinstance(value, m.BitKind):
        return value
    raise NotImplementedError(value, params)


class Generator3Meta(abc.ABCMeta):
    def __new__(metacls, name, bases, namespace):
        namespace = dict(namespace)
        cls = super().__new__(metacls, name, bases, namespace)
        return dataclasses.dataclass(cls)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        return CustomNamespace()


class Generator3(metaclass=Generator3Meta):
    def interface(self):
        ports = {}
        for k, v in self.template.ports.items():
            typ = elaborate_type(v, self)
            if typ is not None:
                ports[k] = typ
        return IO(**ports)
        
    @abc.abstractmethod
    def elaborate(self):
        raise NotImplementedError()

    def __post_init__(self):
        self.elaborate()
        if not hasattr(self, "IO"):
            raise Exception("Must set IO")


m.IO = IO
m.Circuit = Circuit
m.Optional = Optional
m.IOTemplate = IOTemplate
m.Generator1 = Generator1
m.Generator2 = Generator2
m.Generator3 = Generator3
