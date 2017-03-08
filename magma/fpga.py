import re
from .bit import Bit
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
                match = re.findall('(.*)\[(\d+)\]', p.name)
                if match:
                    name, i = match[0]
                    i = int(i)
                    if name in arrays:
                        arrays[name] = max(arrays[name], i)
                    else:
                        arrays[name] = i

        # collect top level module arguments
        args = []
        for p in self.pins:
            if p.used:
                match = re.findall('(.*)\[(\d+)\]', p.name)
                if match:
                    name, i = match[0]
                    i = int(i)
                    if name in arrays and i == 0:
                        args.append('%s %s' % (p.direction, name))
                        args.append(Array(arrays[name]+1, Bit))
                else:
                    args.append('%s %s' % (p.direction, p.name))
                    args.append(Bit)

        D = DefineCircuit('main',*args)
        D.fpga = self
        for p in self.peripherals:
            if p.used:
                #print(p)
                p.setup(D)
        return D

