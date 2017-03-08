from magma import *

def test():
    A2 = Tuple(x=Bit, y=Bit)

    # constructor

    a = A2(name='a')
    print('created A2')
    assert isinstance(a, TupleType)
    assert str(a) == 'a'

    # selectors

    print('a["x"]')
    b = a['x']
    assert isinstance(b, BitType)
    assert str(b) == 'a.x'

    print('a.x')
    b = a.x
    assert isinstance(b, BitType)
    assert str(b) == 'a.x'
