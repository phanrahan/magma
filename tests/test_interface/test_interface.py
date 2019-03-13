from magma import *
"""
http://doc.pytest.org/en/latest/capture.html#accessing-captured-output-from-a-test-function
Uses pytest API for reading stdout/stderr for testing
"""

def test_1():
    I0 = DeclareInterface("a", In(Bit), "b", Out(Bits[2]))
    assert str(I0) == '"a", In(Bit), "b", Out(Bits(2))'

    i0 = I0()
    print(i0)
    assert str(i0) == '"a", In(Bit), "b", Out(Bits(2))'


