import weakref

from hwtypes import BitVector

from magma.circuit import (
    Circuit,
    DefineCircuitKind,
    DebugCircuit,
    DebugDefineCircuitKind,
    NamerDict,
)
from magma.common import ParamDict
from magma.config import config
from magma.debug import get_debug_info


def _make_key(cls, *args, **kwargs):
    _SECRET_KEY = "__magma_generator_secret_key__"
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
    dummy = type.__new__(cls, "", (), {
        "_namer_dict": NamerDict()
    })
    name = cls.__name__
    bases = (cls._base_cls_,)
    dct = cls._base_metacls_.__prepare__(name, bases)
    cls.__init__(dummy, *args, **kwargs)
    dct.update(dict(dummy.__dict__))
    ckt = cls._base_metacls_.__new__(cls, name, bases, dct)
    ckt._args_ = args
    ckt._kwargs_ = kwargs
    return ckt


class _GeneratorMeta(type):
    _cache = weakref.WeakValueDictionary()
    _base_cls_ = Circuit
    _base_metacls_ = DefineCircuitKind

    def __new__(metacls, name, bases, dct):
        bases = bases + (metacls._base_metacls_,)
        return type.__new__(metacls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        # NOTE(leonardt): This is a hacky way to determine that this is a
        # type(...) call, i.e. it is invoked in the class creation pipeline. In
        # that case, there are exactly 3 arguments of the form name, bases, dct.
        # In theory, it would be possible for a Generator subclass to have the
        # same argument number and types, but having the "__module__" member of
        # the dct would be highly unlikely, furthmore they should be using a
        # hashable dict, so it shouldn't satisfy that check. Note that this is
        # why we use "type is" instead of isinstance.
        is_base_cls = (
            len(args) == 3
            and type(args[0]) is str
            and type(args[1]) is tuple
            and (type(args[2]) is dict or type(args[2]) is NamerDict)
            and "__module__" in args[2]
        )
        if is_base_cls:
            return type.__new__(cls, *args)
        if not getattr(cls, "_cache_", True):
            return _make_type(cls, *args, **kwargs)
        key = _make_key(cls, *args, **kwargs)
        try:
            return _GeneratorMeta._cache[key]
        except KeyError:
            pass
        this = _make_type(cls, *args, **kwargs)
        _GeneratorMeta._cache[key] = this
        return this


GeneratorKind = _GeneratorMeta


class Generator(metaclass=_GeneratorMeta):
    def __new__(metacls, name, bases, dct):
        return type.__new__(metacls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if "debug_info" not in kwargs:
            kwargs["debug_info"] = get_debug_info(3)
        return type(cls)._base_metacls_.__call__(cls, *args, **kwargs)

    def __setattr__(cls, key, value):
        if config.use_namer_dict:
            cls._namer_dict[key] = value
        super().__setattr__(key, value)


class _DebugGeneratorMeta(_GeneratorMeta):
    _base_cls_ = DebugCircuit
    _base_metacls_ = DebugDefineCircuitKind


class DebugGenerator(Generator, metaclass=_DebugGeneratorMeta):
    pass


def reset_generator_cache():
    _GeneratorMeta._cache = weakref.WeakValueDictionary()
