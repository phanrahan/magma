import magma as m
from riscv_mini.nasti import (make_NastiIO, NastiParameters,
                              NastiReadAddressChannel)
from riscv_mini.core import make_HostIO, Core
from riscv_mini.cache import Cache


class MemArbiter(m.Generator2):
    def __init__(self, x_len):
        nasti_params = NastiParameters(data_bits=64, addr_bits=x_len,
                                       id_bits=5)
        self.io = m.IO(
            icache=m.Flip(make_NastiIO(nasti_params)),
            dcache=m.Flip(make_NastiIO(nasti_params)),
            nasti=make_NastiIO(nasti_params)
        ) + m.ClockIO(has_reset=True)

        class State(m.Enum):
            IDLE = 0
            ICACHE_READ = 1
            DCACHE_READ = 2
            DCACHE_WRITE = 3
            DCACHE_ACK = 4

        state = m.Register(init=State.IDLE)()

        # write address
        self.io.nasti.aw.data @= self.io.dcache.aw.data
        self.io.nasti.aw.valid @= (self.io.dcache.aw.valid &
                                   (state.O == State.IDLE))
        self.io.dcache.aw.ready @= (self.io.nasti.aw.ready &
                                    (state.O == State.IDLE))
        self.io.icache.aw.ready @= 0

        # write data
        self.io.nasti.w.data @= self.io.dcache.w.data
        self.io.nasti.w.valid @= (self.io.dcache.w.valid &
                                  (state.O == State.DCACHE_WRITE))
        self.io.dcache.w.ready @= (self.io.nasti.w.ready &
                                   (state.O == State.DCACHE_WRITE))
        self.io.icache.w.ready @= 0

        # write ack
        self.io.dcache.b.data @= self.io.nasti.b.data
        self.io.dcache.b.valid @= (self.io.nasti.b.valid &
                                   (state.O == State.DCACHE_ACK))
        self.io.nasti.b.ready @= (self.io.dcache.b.ready &
                                  (state.O == State.DCACHE_ACK))
        self.io.icache.b.valid @= 0
        self.io.icache.b.data.resp @= 0
        self.io.icache.b.data.id @= 0
        self.io.icache.b.data.user @= 0

        # read address
        self.io.nasti.ar.data @= NastiReadAddressChannel(
            nasti_params,
            m.mux([self.io.icache.ar.data.id, self.io.dcache.ar.data.id],
                  self.io.dcache.ar.valid),
            m.mux([self.io.icache.ar.data.addr, self.io.dcache.ar.data.addr],
                  self.io.dcache.ar.valid),
            m.mux([self.io.icache.ar.data.size, self.io.dcache.ar.data.size],
                  self.io.dcache.ar.valid),
            m.mux([self.io.icache.ar.data.length,
                   self.io.dcache.ar.data.length],
                  self.io.dcache.ar.valid),
        )
        self.io.nasti.ar.valid @= ((self.io.icache.ar.valid |
                                    self.io.dcache.ar.valid) &
                                   ~self.io.nasti.aw.valid.value() &
                                   (state.O == State.IDLE))
        self.io.dcache.ar.ready @= (self.io.nasti.ar.ready &
                                    ~self.io.nasti.aw.valid.value() &
                                    (state.O == State.IDLE))
        self.io.icache.ar.ready @= (self.io.dcache.ar.ready.value() &
                                    ~self.io.dcache.ar.valid)

        # read data
        self.io.icache.r.data @= self.io.nasti.r.data
        self.io.dcache.r.data @= self.io.nasti.r.data
        self.io.icache.r.valid @= (self.io.nasti.r.valid &
                                   (state.O == State.ICACHE_READ))
        self.io.dcache.r.valid @= (self.io.nasti.r.valid &
                                   (state.O == State.DCACHE_READ))
        self.io.nasti.r.ready @= ((self.io.icache.r.ready &
                                   (state.O == State.ICACHE_READ)) |
                                  (self.io.dcache.r.ready &
                                   (state.O == State.DCACHE_READ)))

        state.I @= state.O
        with m.when(state.O == State.IDLE):
            with m.when(self.io.dcache.aw.valid &
                        self.io.dcache.aw.ready.value()):
                state.I @= State.DCACHE_WRITE
            with m.elsewhen(self.io.dcache.ar.valid &
                            self.io.dcache.ar.ready.value()):
                state.I @= State.DCACHE_READ
            with m.elsewhen(self.io.icache.ar.valid &
                            self.io.icache.ar.ready.value()):
                state.I @= State.ICACHE_READ
        with m.elsewhen(state.O == State.ICACHE_READ):
            with m.when(self.io.nasti.r.fired() & self.io.nasti.r.data.last):
                state.I @= State.IDLE
        with m.elsewhen(state.O == State.DCACHE_READ):
            with m.when(self.io.nasti.r.fired() & self.io.nasti.r.data.last):
                state.I @= State.IDLE
        with m.elsewhen(state.O == State.DCACHE_WRITE):
            with m.when(self.io.dcache.w.valid &
                        self.io.dcache.w.ready.value() &
                        self.io.dcache.w.data.last):
                state.I @= State.DCACHE_ACK
        with m.elsewhen(state.O == State.DCACHE_ACK):
            with m.when(self.io.nasti.b.fired()):
                state.I @= State.IDLE


class Tile(m.Generator2):
    def __init__(self, x_len):
        nasti_params = NastiParameters(data_bits=64, addr_bits=x_len,
                                       id_bits=5)

        self.io = m.IO(
            host=make_HostIO(x_len),
            nasti=make_NastiIO(nasti_params)
        ) + m.ClockIO(has_reset=True)

        core = Core(x_len)()
        n_sets = 256
        b_bytes = 4 * (x_len >> 3)
        icache = Cache(x_len, 1, n_sets, b_bytes)()
        dcache = Cache(x_len, 1, n_sets, b_bytes)()
        arb = MemArbiter(x_len)()

        self.io.host @= core.host
        core.icache @= icache.cpu
        core.dcache @= dcache.cpu
        arb.icache @= icache.nasti
        arb.dcache @= dcache.nasti
        self.io.nasti @= arb.nasti
