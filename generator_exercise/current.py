import magma as m
import common


def generate_add(bits, has_ce):
    ports = dict(I0=m.In(m.UInt[bits]),
                 I1=m.In(m.UInt[bits]),
                 O=m.Out(m.UInt[bits]))
    if has_ce:
        ports.update(dict(CE=m.In(m.Bit)))

    class _Add(m.Circuit):
        name = f"Add_{bits}_{has_ce}"
        IO = m.IO(**ports)

        out = IO.I0 + IO.I1
        if has_ce:
            out += m.zext(m.uint(IO.CE), bits - 1)
        m.wire(out, IO.O)

    return _Add


Add16 = generate_add(16, False)
Add8_CE = generate_add(8, True)
