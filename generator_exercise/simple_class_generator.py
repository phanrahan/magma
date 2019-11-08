import magma as m
import common


class Add(m.Generator1):
    bits: int
    has_ce: bool

    def generate(self):
        ports = dict(I0=m.In(m.UInt[self.bits]),
                     I1=m.In(m.UInt[self.bits]),
                     O=m.Out(m.UInt[self.bits]))
        if self.has_ce:
            ports.update(dict(CE=m.In(m.Bit)))

        class _Add(m.Circuit):
            name = f"Add_{self.bits}_{self.has_ce}"
            IO = m.IO(**ports)

            out = IO.I0 + IO.I1
            if self.has_ce:
                out += m.zext(m.uint(IO.CE), self.bits - 1)
            m.wire(out, IO.O)

        return _Add


Add16Gen = Add(16, False)
Add16 = Add16Gen.generate()
Add8_CEGen = Add(8, True)
Add8_CE = Add8_CEGen.generate()
