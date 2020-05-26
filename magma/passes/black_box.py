from typing import Iterable

from magma.circuit import CircuitKind
from magma.passes.passes import CircuitPass


class BlackBoxPass(CircuitPass):
    def __init__(self, main: CircuitKind, black_boxes: Iterable[CircuitKind]):
        super().__init__(main)
        self._black_boxes = set(black_boxes)

    def __call__(self, cls):
        try:
            self._black_boxes.remove(cls)
        except KeyError:
            return  # @cls not in black_boxes, don't need to do anything
        cls._is_definition = False
