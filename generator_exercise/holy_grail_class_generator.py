import magma as m
import common


class Add(m.Generator3):
    bits: int
    has_ce: bool

    template = m.IOTemplate(
        I0=m.In(m.UInt[bits]),
        I1=m.In(m.UInt[bits]),
        O=m.Out(m.UInt[bits]),
        CE=m.Optional(has_ce, m.In(m.Bit))
    )

    def elaborate(self):
        self.name = f"Add_{self.bits}_{self.has_ce}"
        self.IO = self.interface()

        out = self.IO.I0 + self.IO.I1
        if self.has_ce:
            out += m.zext(m.uint(self.IO.CE), self.bits - 1)
        m.wire(out, self.IO.O)


Add16 = Add(16, False)
Add8_CE = Add(8, True)


# Want to be able to do this!
#   x = m.UInt[24]()
#   y = m.UInt[24]()
#   out = Add(x, y)
