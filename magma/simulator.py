from abc import ABC, abstractmethod

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
