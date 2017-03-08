from .circuit import CircuitType

class Peripheral(CircuitType):

    """A single peripheral on an fpga  (like a Clock, a Timer, or a USART)"""

    def __init__(self, fpga, name=""):
        super(Peripheral, self).__init__(name=name)

        self.fpga = fpga
        if fpga:
            fpga.place(self)

    def setup(self, main):
        pass

