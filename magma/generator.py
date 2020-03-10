from abc import abstractmethod, ABCMeta
import collections
import functools
from .circuit import DefineCircuitKind, Circuit


class ParamDict(dict):
    """
    Hashable dictionary for simple key: value parameters
    """
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class GeneratorMeta(type):
    def __new__(mcs, name, bases, attrs):
        attrs["bind_generators"] = []
        cls = super().__new__(mcs, name, bases, attrs)
        if cls.cache:
            cls.generate = functools.lru_cache(maxsize=None)(cls.generate)

        old_generate = cls.generate

        def generate_wrapper(*args, **kwargs):
            result = old_generate(*args, **kwargs)
            if hasattr(result, "circuit_definition"):
                result = result.circuit_definition
            for gen in cls.bind_generators:
                gen.generate_bind(result, *args, **kwargs)
            return result

        cls.generate = generate_wrapper
        return cls

    def __call__(cls, *args, name=None, **kwargs):
        """
        name is reserved kwarg for naming instances

        TODO: Generalize handling of instance parameters
        """
        inst_kwargs = {}
        if name is not None:
            inst_kwargs["name"] = name
        return cls.generate(*args, **kwargs)(**inst_kwargs)


class Generator(metaclass=GeneratorMeta):
    # User can disable cacheing by setting this attribute to False
    cache = True

    @staticmethod
    @abstractmethod
    def generate(*args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def bind(cls, monitor):
        cls.bind_generators.append(monitor)


class _Generator2Meta(type):
    def __new__(metacls, name, bases, dct):
        bases = bases + (DefineCircuitKind,)
        return type.__new__(metacls, name, bases, dct)

    def __call__(*args, **kwargs):
        cls = args[0]
        args = args[1:]
        if cls is Generator2:
            try:
                name, bases, dct = args
            except ValueError:
                raise Exception("Can not initialize base Generator class")
            assert not kwargs
            return type.__new__(cls, name, bases, dct)
        dummy = type.__new__(cls, "", (), {})
        name = cls.__name__
        bases = (Circuit,)
        dct = DefineCircuitKind.__prepare__(name, bases)
        cls.__init__(dummy, *args, **kwargs)
        dct.update(dict(dummy.__dict__))
        t = DefineCircuitKind.__new__(cls, name, bases, dct)
        return t


class Generator2(metaclass=_Generator2Meta):
    def __new__(metacls, name, bases, dct):
        return type.__new__(metacls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        return DefineCircuitKind.__call__(cls, *args, **kwargs)
