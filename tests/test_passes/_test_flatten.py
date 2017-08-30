import os
os.environ['MANTLE_TARGET'] = 'ice40'
from mantle.lattice.mantle40.adder  import DefineAdders
from mantle import DefineCounter
from mantle.lattice.ice40 import SB_LUT4, SB_CARRY, SB_DFF
from magma.passes import InstancePass, DefinitionPass
from magma.transforms import flatten, setup_clocks

class PrimitivesPass(InstancePass):
    def __init__(self, main):
        super(PrimitivesPass, self).__init__(main)
        self.nluts = 0
        self.ncarrys = 0
        self.ndffs = 0

    def __call__(self, instance):
        if isinstance(instance, SB_LUT4):
            self.nluts += 1
        elif isinstance(instance, SB_CARRY):
            self.ncarrys += 1
        elif isinstance(instance, SB_DFF):
            self.ndffs += 1

def test_adder():
    add = DefineAdders(8, False, False)
    print(repr(add))
    c = flatten(add).circuit
    print(repr(c))
    p = PrimitivesPass(c).run()
    assert p.nluts == 8

def test_counter():
    Counter8 = DefineCounter(8)
    print(repr(Counter8))
    print()
    setup_clocks(Counter8)
    c = flatten(Counter8).circuit
    #print(type(c))
    print(repr(c))
    p = PrimitivesPass(c).run()
    assert p.nluts == 8
    print('nluts =',p.nluts)
    print('ncarrys =',p.ncarrys)
    print('ndffs =',p.ndffs)


