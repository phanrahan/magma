import magma as m


def test_circuit():

    class _Foo(m.Circuit):
        io = m.IO(
            I0=m.In(m.SmartBits[7]),
            I1=m.In(m.SmartBits[9]),
            O=m.Out(m.SmartBits[10]),
            O2=m.Out(m.SmartBits[16]),
            O3=m.Out(m.SmartBit),
        )
        x = io.I0 + io.I1 + io.I1
        io.O @= x
        io.O2 @= x
        io.O3 @= io.I0

    m.compile("Foo", _Foo, output="coreir")


def test_basic():
    def x_():
        return m.SmartBits[10]()

    def y_():
        return m.SmartBits[16]()

    def z_():
        return m.SmartBit()

    class Foo(m.Circuit):

        x = x_()
        y = y_()
        z = z_()

        # Any Smart<x> can be wired to any Smart<y>.
        x @= y  # truncate y
        y @= x  # extend x
        #x @= z  # promote z to SmartBits[1], then extend z
        #z @= x  # promote z to SmartBits[1], then truncate x

        # Any Smart<x> (op) Smart<y> is valid; each (op) has its own width rules.
        # Arithmetic and logic.
        x @= x + y  # out width = max(10, 16) = 16; op is +, -, *, /, %, &, |, ^
        #x + z  # promote z to SmartBits[1]; out width = max(1, 10) = 10
        ~x  # out width = 10; ~
        #~z  # out = SmartBit
        #z + z  # promote *both* z's to SmartBits[1], then extract LSB;
               # out = SmartBit

        # Comparison.
        x <= y  # out = SmartBit; op is ==, !=, <, <=, >, >=, reduction

        # Shifting
        x << y  # extend x, truncate output; out width = 10; op is <<, >>
        y << x  # extend x; out width = 16
        #x << z  # promote z to SmartBits[1], extend z; out width = 10
        #z << x  # promote z to SmartBits[1], extend z, truncate output;
                # out = SmartBit

        # Any (op) Smart<x> is valid (unary op); (op)'s follow simple width rules.
        ~x  # out width = 10
        #~z  # out = SmartBit

        # Context-determined operators.
