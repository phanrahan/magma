import os
os.environ['MANTLE_TARGET'] = 'ice40'
from magma.passes import InstanceGraphPass
from mantle import DefineCounter

class PrintInstanceGraphPass(InstanceGraphPass):
    def __call__(self, definition, dependencies):
        print(definition)

def test_counter():
    Counter8 = DefineCounter(8)
    PrintInstanceGraphPass(Counter8).run()

test_counter()
