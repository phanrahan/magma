import os
os.environ['MANTLE_TARGET'] = 'ice40'
from mantle import DefineCounter
from magma.passes import InstancePass, DefinitionPass
from magma.passes.ir import IRPass

def test_definition():
    counter = DefineCounter(8)
    p = DefinitionPass(counter)
    p.run()
    print(len(p.definitions))

def test_instance():
    counter = DefineCounter(8)
    print(repr(counter))
    p = InstancePass(counter)
    p.run()
    print(len(p.instances))

def test_ir():
    counter = DefineCounter(8)
    p = IRPass(counter).run()
    print(p.code)

