from mantle import mux
import magma as m


class txmod_logic(m.Circuit):
    IO = ['data', m.In(m.Bits(8)), 'writing', m.In(m.Bit), 'valid', m.In(m.
        Bit), 'dataStore', m.In(m.Bits(11)), 'writeClock', m.In(m.Bits(14)),
        'writeBit', m.In(m.Bits(4)), 'O0', m.Out(m.Bit), 'O1', m.Out(m.Bits
        (11)), 'O2', m.Out(m.Bits(14)), 'O3', m.Out(m.Bits(4)), 'O4', m.Out
        (m.Bit)]

    @classmethod
    def definition(io):
        writing_out = mux([mux([mux([mux([io.writing, io.writing], io.
            writing == m.bit(1)), io.writing], (io.writing == m.bit(1)) & (
            io.writeClock == m.bits(0, 14))), m.bit(0)], (io.writing == m.
            bit(1)) & (io.writeClock == m.bits(0, 14)) & (io.writeBit == m.
            bits(9, 4))), m.bit(1)], (io.writing == m.bit(0)) & (io.valid ==
            m.bit(0)))
        dataStore_out = mux([mux([mux([mux([io.dataStore, io.dataStore], io
            .writing == m.bit(1)), io.dataStore], (io.writing == m.bit(1)) &
            (io.writeClock == m.bits(0, 14))), io.dataStore], (io.writing ==
            m.bit(1)) & (io.writeClock == m.bits(0, 14)) & (io.writeBit ==
            m.bits(9, 4))), m.concat(io.dataStore[0:1], io.data, io.
            dataStore[9:])], (io.writing == m.bit(0)) & (io.valid == m.bit(0)))
        writeClock_out = mux([mux([mux([mux([io.writeClock, m.bits(m.uint(
            io.writeClock) - m.bits(1, 14))], io.writing == m.bit(1)), m.
            bits(100, 14)], (io.writing == m.bit(1)) & (io.writeClock == m.
            bits(0, 14))), io.writeClock], (io.writing == m.bit(1)) & (io.
            writeClock == m.bits(0, 14)) & (io.writeBit == m.bits(9, 4))),
            m.bits(100, 14)], (io.writing == m.bit(0)) & (io.valid == m.bit(0))
            )
        writeBit_out = mux([mux([mux([mux([io.writeBit, io.writeBit], io.
            writing == m.bit(1)), m.bits(m.uint(io.writeBit) + m.bits(1, 4)
            )], (io.writing == m.bit(1)) & (io.writeClock == m.bits(0, 14))
            ), io.writeBit], (io.writing == m.bit(1)) & (io.writeClock == m
            .bits(0, 14)) & (io.writeBit == m.bits(9, 4))), m.bits(0, 4)], 
            (io.writing == m.bit(0)) & (io.valid == m.bit(0)))
        TXReg_out = mux([mux([mux([mux([m.bit(1), io.dataStore[io.writeBit]
            ], io.writing == m.bit(1)), io.dataStore[io.writeBit]], (io.
            writing == m.bit(1)) & (io.writeClock == m.bits(0, 14))), m.bit
            (1)], (io.writing == m.bit(1)) & (io.writeClock == m.bits(0, 14
            )) & (io.writeBit == m.bits(9, 4))), io.dataStore[0]], (io.
            writing == m.bit(0)) & (io.valid == m.bit(0)))
        O0, O1, O2, O3, O4 = (writing_out, dataStore_out, writeClock_out,
            writeBit_out, TXReg_out)
        m.wire(O0, io.O0)
        m.wire(O1, io.O1)
        m.wire(O2, io.O2)
        m.wire(O3, io.O3)
        m.wire(O4, io.O4)
