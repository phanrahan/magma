from magma import *

def test():
    b = BitIn(name="a")
    assert str(b) == "a"
    assert isinstance(b, BitIn)
    assert b.isinput()

    b = BitOut(name="a")
    assert str(b) == "a"
    assert isinstance(b, BitOut)
    assert b.isoutput()

    b = Bit(name="a")
    assert str(b) == "a"
    assert isinstance(b, Bit)
    assert not b.isinput()
    assert not b.isoutput()
    assert not b.isinout()
