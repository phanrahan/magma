from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
import inspect
import typing
from collections import OrderedDict, UserDict


__all__  = ["GeneratorBase"]
__all__ += ["wrap_generator"]


_ANNOTATIONS = "__annotations__"


class _AnnotationsDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def __setitem__(self, key, value):
        print ("ANN set item", key, value)
        super().__setitem__(key, value)


class _MetaDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        super().__setitem__(_ANNOTATIONS, _AnnotationsDict())

    def __getitem__(self, key):
        if key == _ANNOTATIONS:
            print ("getting annotations!!")
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key == _ANNOTATIONS:
            return
        return super().__setitem__(key, value)

    def as_dict(self):
        return dict(self)


class _GeneratorMeta(type):
    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        return cls

    def __call__(cls, *args, **kwargs):
        io = cls.__new__(cls, *args, **kwargs)
        defn = magma.DefineCircuit(

    def __getitem__(cls, *args):
        return None


class GeneratorBase(metaclass=_GeneratorMeta):
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
