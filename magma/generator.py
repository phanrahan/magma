from abc import abstractmethod
import functools
import collections


class ParamDict(dict):
    """
    Hashable dictionary for simple key: value parameters
    """
    def __hash__(self):
        return hash(tuple(sorted(self.keys())))


class GeneratorMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if cls.cache:
            cls.generate = functools.lru_cache(maxsize=None)(cls.generate)
        return cls

    def __call__(cls, *args, **kwargs):
        return cls.generate(*args, **kwargs)()


class Generator(metaclass=GeneratorMeta):
    # User can disable cacheing by setting this attribute to False
    cache = True
    __circuit_cache = {}

    @staticmethod
    @abstractmethod
    def generate(*args, **kwargs):
        raise NotImplementedError()
