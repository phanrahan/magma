from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
import inspect
import typing
from collections import OrderedDict


__all__  = ["GeneratorBase"]
__all__ += ["wrap_generator"]


class _DataclassMeta(ABCMeta):
    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        cls = dataclass(cls)
        cls._cache_ = {}

        elaborate = cls.elaborate
        if getattr(elaborate, "__isabstractmethod__", False):
            return cls

        fields = cls.__dataclass_fields__
        def _elaborate_wrapped(self_):
            key = frozenset({getattr(self_, f) for f in fields})
            elaborated = cls._cache_.get(key, None)
            if elaborated is None:
                elaborated = elaborate(self_)
                cls._cache_[key] = elaborated
            return elaborated
        cls.elaborate = _elaborate_wrapped

        return cls


class GeneratorBase(metaclass=_DataclassMeta):
    @abstractmethod
    def elaborate(self):
        pass


def wrap_generator(generator, name=None):
    sig = inspect.signature(generator)
    params = OrderedDict()
    defaults = OrderedDict()
    for param_name, param in sig.parameters.items():
        typ = typing.Any
        if param.annotation is not inspect.Parameter.empty:
            typ = param.annotation
        params[param_name] = typ
        if param.default is not inspect.Parameter.empty:
            defaults[param_name] = param.default
    if name is None:
        name = generator.__name__
    bases = (GeneratorBase,)
    def _elaborate(self_):
        args = [getattr(self_, p) for p in sig.parameters]
        return generator(*args)
    dct = {
        "elaborate": _elaborate,
        "__annotations__": dict(params),
        "__module__": generator.__module__,
    }
    dct.update(defaults)
    cls = type(name, bases, dct)
    return dataclass(cls)
