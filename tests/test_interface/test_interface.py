from magma import *
"""
http://doc.pytest.org/en/latest/capture.html#accessing-captured-output-from-a-test-function
Uses pytest API for reading stdout/stderr for testing
"""

def test_1(capsys):
    I0 = DeclareInterface("input a", Bit, "output b", Array2)
    print(I0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "Interface[input a, Bit, output b, Array(2,Bit)]"

    i0 = I0()
    print(i0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "a : In(Bit) -> b : Array(2,Out(Bit))"

def test_2(capsys):
    I0 = DeclareInterface("a", In(Bit), "b", Out(Array2))
    print(I0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "Interface[a, In(Bit), b, Array(2,Out(Bit))]"

    i0 = I0()
    print(i0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "a : In(Bit) -> b : Array(2,Out(Bit))"

def test_3(capsys):
    I0 = DeclareInterface("input a", In(Bit), "output b", Out(Array2))
    print(I0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "Interface[input a, In(Bit), output b, Array(2,Out(Bit))]"

    i0 = I0()
    print(i0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "a : In(Bit) -> b : Array(2,Out(Bit))"

def test_4(capsys):
    I0 = DeclareInterface("input a", In(Bit), "input b", Out(Array2))
    print(I0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "Interface[input a, In(Bit), input b, Array(2,Out(Bit))]"

    i0 = I0()
    print(i0)
    out, err = capsys.readouterr()
    assert out.rstrip() == "Warning: directions inconsistent input output\na : In(Bit), b : Array(2,In(Bit)) ->"
