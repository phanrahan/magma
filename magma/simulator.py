import sys
from abc import abstractmethod
if sys.version_info < (3, 4):
    import abc
    ABC = abc.ABCMeta('ABC', (object,), {})
else:
    from abc import ABC

class CircuitSimulator(ABC):
    @abstractmethod
    def __init__(self, circuit):
        pass

    @abstractmethod
    def get_capabilities(self):
        pass

    @abstractmethod
    def get_value(self, bit, scope):
        pass

    @abstractmethod
    def set_value(self, bit, scope, newval):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def step(self):
        pass
