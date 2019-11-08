import magma as m
import common

class Add(m.Generator2):
    bits: int
    has_ce: bool

    def elaborate(self):
        ports = dict(I0=m.In(m.UInt[self.bits]),
                     I1=m.In(m.UInt[self.bits]),
                     O=m.Out(m.UInt[self.bits]))
        if self.has_ce:
            ports.update(dict(CE=m.In(m.Bit)))

        self.name = f"Add_{self.bits}_{self.has_ce}"
        self.IO = m.IO(**ports)

        out = self.IO.I0 + self.IO.I1
        if self.has_ce:
            out += m.zext(m.uint(self.IO.CE), self.bits - 1)
        m.wire(out, self.IO.O)


Add16 = Add(16, False)
Add8_CE = Add(8, True)
