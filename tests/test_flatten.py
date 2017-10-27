import magma
from magma import *
from collections import OrderedDict

def test_flatten():
    b0 = Bit(name='b0')
    b1 = Bit(name='b1')
    b2 = Bit(name='b2')
    b3 = Bit(name='b3')
    b4 = Bit(name='b4')
    a1 = array([b0, b1])
    a2 = array([b0, b1])
    assert a1 is not a2, "They are different type objects"
    assert [t1 is t2 for t1, t2 in zip(a1, a2)], "Subtypes are the same"
    A = Array(2,Bit)
    B = Array(2,Bit)
    assert A is B
    d = dict(x=array([b0, b1]), y=array([b2, b3, b4]))
    t = tuple_(OrderedDict(sorted(d.items(), key=lambda t: t[0])))
    assert str(t.name) == "None"
    assert str(type(t)) == "Tuple(x=Array(2,Bit),y=Array(3,Bit))"
    a = array(t.flatten())
    assert str(a.name) == "None"
    assert str(type(a)) == "Array(5,Bit)"

test_flatten()
