from abc import ABC, abstractmethod
from enum import Enum, auto


class Determination(Enum):
    SELF_DETERMINED = auto()
    CONTEXT_DETERMINED = auto()


class Context:
    pass


class Op(ABC):
    def __init__(self, determination: Determination):
        self._determination = determination
    
    @abstractmethod
    def __call__(self, context: Context, *args):
        raise NotImplementedError


class ContextualBinOp(Op):
    def __init__(self, op):
        super().__init__(CONTEXT_DETERMINED)
        self._op = op

    def __call__(self, context, lhs, rhs):
        pass
