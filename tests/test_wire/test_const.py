from magma import *
from magma.testing import check_files_equal


def test_bit_0():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    wire(0, buf.I)
    wire(buf.O, main.O)

    compile("build/bit_0", main)
    assert check_files_equal(__file__, "build/bit_0.v", "gold/bit_0.v")


def test_bit_1():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    compile("build/bit_1", main)
    assert check_files_equal(__file__, "build/bit_1.v", "gold/bit_1.v")


def test_bits_0():
    T = Bits(4)
    Buf = DeclareCircuit('Buf', "I", In(T), "O", Out(T))

    main = DefineCircuit("main", "O", Out(T))

    buf = Buf()

    wire(0, buf.I)
    wire(buf.O, main.O)

    compile("build/bits_0", main)
    assert check_files_equal(__file__, "build/bits_0.v", "gold/bits_0.v")

def test_bits_1():
    T = Bits(4)
    Buf = DeclareCircuit('Buf', "I", In(T), "O", Out(T))

    main = DefineCircuit("main", "O", Out(T))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    compile("build/bits_1", main)
    assert check_files_equal(__file__, "build/bits_1.v", "gold/bits_1.v")

def test_uint_0():
    T = UInt(4)
    Buf = DeclareCircuit('Buf', "I", In(T), "O", Out(T))

    main = DefineCircuit("main", "O", Out(T))

    buf = Buf()

    wire(0, buf.I)
    wire(buf.O, main.O)

    compile("build/uint_0", main)
    assert check_files_equal(__file__, "build/uint_0.v", "gold/uint_0.v")

def test_uint_1():
    T = UInt(4)
    Buf = DeclareCircuit('Buf', "I", In(T), "O", Out(T))

    main = DefineCircuit("main", "O", Out(T))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    compile("build/uint_1", main)
    assert check_files_equal(__file__, "build/uint_1.v", "gold/uint_1.v")

def test_sint_0():
    T = SInt(4)
    Buf = DeclareCircuit('Buf', "I", In(T), "O", Out(T))

    main = DefineCircuit("main", "O", Out(T))

    buf = Buf()

    wire(0, buf.I)
    wire(buf.O, main.O)

    compile("build/sint_0", main)
    assert check_files_equal(__file__, "build/sint_0.v", "gold/sint_0.v")

def test_sint_1():
    T = SInt(4)
    Buf = DeclareCircuit('Buf', "I", In(T), "O", Out(T))

    main = DefineCircuit("main", "O", Out(T))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    compile("build/sint_1", main)
    assert check_files_equal(__file__, "build/sint_1.v", "gold/sint_1.v")

