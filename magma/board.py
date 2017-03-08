from .circuit import CircuitType

class Board(CircuitType):
    def __init__(self, name):
        super(Board, self).__init__(name=name)
        self.parts = []

    def place(self, part):
        self.parts.append(part)
        part.board = self


