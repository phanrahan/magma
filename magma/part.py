from .circuit import CircuitType

class Part(CircuitType):

    """A single component (like a LED, transistor, IC, MCU, FPGA)"""

    def __init__(self, name="", board=None):
        super(Part, self).__init__(name=name)
        self.pins = []

        self.board = board
        if board:
            board.place(self)

    def setup(self, main):
        pass
