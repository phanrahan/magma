from magma import *

def test_flatten():
    b0 = Bit(name='b0')
    b1 = Bit(name='b1')
    b2 = Bit(name='b2')
    b3 = Bit(name='b3')
    b4 = Bit(name='b4')
    a1 = array([b0, b1])
    a2 = array([b0, b1])
    print(a1==a2)
    A = Array[2,Bit]
    B = Array[2,Bit]
    print(A==B)
    t = tuple_(dict(x=array([b0, b1]), y=array([b2, b3, b4])))
    print(type(t.name))
    print(type(t))
    a = array(t.flatten())
    print(a.name)
    print(type(a))
