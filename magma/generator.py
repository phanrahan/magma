from abc import abstractmethod, ABCMeta
import collections
import functools
import weakref
from .circuit import (DefineCircuitKind, Circuit, DebugCircuit,
                      DebugDefineCircuitKind)
from . import cache_definition
from magma.common import ParamDict
from hwtypes import BitVector


class GeneratorMeta(type):
    def __new__(mcs, name, bases, attrs):
        attrs["bind_generators"] = []
        cls = super().__new__(mcs, name, bases, attrs)
        old_generate = cls.generate

        def generate_wrapper(*args, **kwargs):
            result = old_generate(*args, **kwargs)
            if hasattr(result, "circuit_definition"):
                result = result.circuit_definition
            for gen in cls.bind_generators:
                gen.generate_bind(result, *args, **kwargs)
            return result

        cls.generate = generate_wrapper
        # Cache after bind logic so we don't run it twice on a cached entry
        if cls.cache:
            cls.generate = cache_definition(cls.generate)
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


def _make_key(cls, *args, **kwargs):
    _SECRET_KEY = "__magma_generator2_secret_key__"
    dct = {f"{_SECRET_KEY}{i}": v for i, v in enumerate(args)}
    dct.update(kwargs)
    for k, v in dct.items():
        if isinstance(v, BitVector):
            # Custom hash for BitVector to avoid inconsistent size error in key
            # comparison
            # TODO(leonardt/array2): We could move this to the BV.__hash__ if
            # this might be more generally useful as a pattern
            dct[k] = (int(v), len(v))
    return (cls, ParamDict(dct))


def _make_type(cls, *args, **kwargs):
    dummy = type.__new__(cls, "", (), {})
    name = cls.__name__
    bases = (cls._base_cls_,)
    dct = cls._base_metacls_.__prepare__(name, bases)
    cls.__init__(dummy, *args, **kwargs)
    dct.update(dict(dummy.__dict__))
    # NOTE(leonardt): We need to override the Generator2 classmethod bind with
    # DefineCircuitKind.bind for generator instances (circuits).
    dct["bind"] = classmethod(cls._base_metacls_.bind)
    ckt = cls._base_metacls_.__new__(cls, name, bases, dct)
    ckt._args_ = args
    ckt._kwargs_ = kwargs
    for gen in cls.bind_generators:
        gen.generate_bind(ckt, *args, **kwargs)
    return ckt


class _Generator2Meta(type):
    _cache = weakref.WeakValueDictionary()
    _base_cls_ = Circuit
    _base_metacls_ = DefineCircuitKind

    def __new__(metacls, name, bases, dct):
        bases = bases + (metacls._base_metacls_,)
        assert dct.setdefault("bind_generators", []) == []
        return type.__new__(metacls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if cls is Generator2:
            try:
                name, bases, dct = args
            except ValueError:
                raise Exception("Can not initialize base Generator class")
            assert not kwargs
            return type.__new__(cls, name, bases, dct)
        if not getattr(cls, "_cache_", True):
            return _make_type(cls, *args, **kwargs)
        key = _make_key(cls, *args, **kwargs)
        try:
            return _Generator2Meta._cache[key]
        except KeyError:
            pass
        this = _make_type(cls, *args, **kwargs)
        _Generator2Meta._cache[key] = this
        return this


Generator2Kind = _Generator2Meta


class Generator2(metaclass=_Generator2Meta):
    def __new__(metacls, name, bases, dct):
        return type.__new__(metacls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        return type(cls)._base_metacls_.__call__(cls, *args, **kwargs)

    @classmethod
    def bind(cls, monitor):
        cls.bind_generators.append(monitor)


class _DebugGeneratorMeta(_Generator2Meta):
    _base_cls_ = DebugCircuit
    _base_metacls_ = DebugDefineCircuitKind


class DebugGenerator2(Generator2, metaclass=_DebugGeneratorMeta):
    pass


def reset_generator_cache():
    _Generator2Meta._cache = weakref.WeakValueDictionary()
