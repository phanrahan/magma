from abc import abstractmethod
import functools
import collections


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
