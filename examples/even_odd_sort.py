import magma as m


class Swap(m.Circuit):
    io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[2]))
    # io.O @= m.bits([io.I.reduce_and(), io.I.reduce_or())
    print(m.fork(m.Bit.And, m.Bit.Or))
    io.O @= m.uncurry(m.fork(m.Bit.And(), m.Bit.Or()))(io.I)
