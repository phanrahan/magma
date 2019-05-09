from .circuit import DefineCircuitKind, Circuit, CircuitType, CircuitKind, IO


class GeneratorKind(type):
    def __new__(metacls, name, bases, dct):
        return super().__new__(metacls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        bases = (Circuit,)
        io = cls.new(*args, **kwargs)
        name = cls.__name__
        return super().__call__(name, bases, {"io": io})


class Generator(DefineCircuitKind, metaclass=GeneratorKind):
    def new():
        return IO()
