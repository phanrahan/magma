from magma import *

def test():
    print('tuple_("x",1,"y",1)')
    a1 = tuple_("x",1,"y",1)
    assert isinstance(a1, TupleType)
