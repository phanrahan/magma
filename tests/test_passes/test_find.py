import os
os.environ['MANTLE_TARGET'] = 'ice40'
from mantle import DefineCounter
from magma.passes.find import find

def test_find():
    counter = DefineCounter(8)
    defn = {}
    find(counter, defn)
    for k, v in defn.items():
        print(k, v)

test_find()
