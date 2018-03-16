import sys
from abc import abstractmethod
from collections import namedtuple
if sys.version_info < (3, 4):
    import abc
    ABC = abc.ABCMeta('ABC', (object,), {})
else:
    from abc import ABC

ExecutionState = namedtuple('ExecutionState', ['cycles', 'clock', 'triggered_points'])

class CircuitSimulator(ABC):
    @abstractmethod
    def __init__(self, circuit, clock):
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
    def advance(self, halfcycles):
        pass

    def advance_cycle(self, cycles=1):
        self.advance(cycles * 2)

    @abstractmethod
    def evaluate(self_):
        pass

    @abstractmethod
    def rewind(self, halfcycles):
        pass

    def rewind_cycle(self, cycles=1):
        self.rewind(cycles * 2)

    @abstractmethod
    def cont(self):
        pass

    @abstractmethod
    def add_watchpoint(self, bit, scope, value=None):
        pass

    @abstractmethod
    def delete_watchpoint(self, num):
        pass

