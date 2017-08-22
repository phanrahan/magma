import re
from .port import INPUT, OUTPUT
from .t import In, Out
from .bit import Bit
from .bits import Bits
from .array import Array
from .circuit import DefineCircuit
from .part import Part

class FPGA(Part):

    """An FPGA"""

    def __init__(self, name='', board=None):
        Part.__init__(self, name, board)
        self.gpios = []
        self.peripherals = []

        self.parts = []

    def place(self, peripheral):
        self.peripherals.append(peripheral)
        peripheral.fpga = self

    def main(self):
        arrays = {}
        # form arrays
        for p in self.pins:
            if p.used:
                # find names of the form %s[%d]
                #  these are considered arrays
                match = re.findall('(.*)\[(\d+)\]', p.name)
                if match:
                    name, i = match[0]
                    i = int(i)
                    # keep track of the maximum index
                    if name in arrays:
                        arrays[name] = max(arrays[name], i)
                    else:
                        arrays[name] = i

        # collect top level module arguments
        args = []
        for p in self.pins:
            if p.used:
                # find names of the form %s[%d]
                #  these are considered arrays
                match = re.findall('(.*)\[(\d+)\]', p.name)
                if match:
                    name, i = match[0]
                    i = int(i)
                    if name in arrays and i == 0:
                        args.append(name)
                        T = Bits(arrays[name]+1)
                        args.append(In(T) if p.direction == INPUT else Out(T))
                else:
                    args.append(p.name)
                    args.append(In(Bit) if p.direction == INPUT else Out(Bit))

        D = DefineCircuit('main',*args)
        D.fpga = self
        for p in self.peripherals:
            if p.used:
                #print(p)
                p.setup(D)
        return D

