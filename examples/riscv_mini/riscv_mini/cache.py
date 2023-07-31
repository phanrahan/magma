import magma as m
from mantle2.counter import Counter
from riscv_mini.nasti import (make_NastiIO, NastiParameters,
                              NastiReadAddressChannel,
                              NastiWriteAddressChannel, NastiWriteDataChannel)
# m.config.set_debug_mode(True)


def make_CacheReq(x_len):
    class CacheReq(m.Product):
        addr = m.UInt[x_len]
        data = m.UInt[x_len]
        mask = m.UInt[x_len // 8]
    return CacheReq


def make_CacheResp(x_len):
    class CacheResp(m.Product):
        data = m.UInt[x_len]
    return CacheResp


def make_CacheIO(x_len):
    class CacheIO(m.Product):
        abort = m.In(m.Bit)
        req = m.In(m.Valid[make_CacheReq(x_len)])
        resp = m.Out(m.Valid[make_CacheResp(x_len)])
    return CacheIO


def make_cache_ports(x_len, nasti_params):
    return {
        "cpu": make_CacheIO(x_len),
        "nasti": make_NastiIO(nasti_params)
    }


class ArrayMaskMem(m.Generator2):
    """
    Wrapper around a memory to store entries containing an array of values that
    can be written using a write mask for each array index

    Implemented using a separate memory for each array index, the mask indices
    are mapped into the WEN ports of each sub-memory
    """

    def __init__(self, height, array_length, T, read_latency, has_read_enable):
        addr_width = m.bitutils.clog2(height)
        self.io = m.IO(
            RADDR=m.In(m.Bits[addr_width]),
            RDATA=m.Out(m.Array[array_length, T]),
        ) + m.ClockIO()
        if has_read_enable:
            self.io += m.IO(RE=m.In(m.Enable))
        self.io += m.IO(
            WADDR=m.In(m.Bits[addr_width]),
            WDATA=m.In(m.Array[array_length, T]),
            WMASK=m.In(m.Bits[array_length]),
            WE=m.In(m.Enable)
        )
        for i in range(array_length):
            mem = m.Memory(height, T, read_latency,
                           has_read_enable=has_read_enable)()
            mem.RADDR @= self.io.RADDR
            if has_read_enable:
                mem.RE @= self.io.RE
            self.io.RDATA[i] @= mem.RDATA

            mem.write(self.io.WDATA[i], self.io.WADDR,
                      m.enable(m.bit(self.io.WE) & self.io.WMASK[i]))

        def read(self, addr, enable=None):
            self.RADDR @= addr
            if enable is not None:
                if not has_read_enable:
                    raise Exception("Cannot use `enable` with no read enable")
                self.RE @= enable
            return self.RDATA

        self.read = read

        def write(self, data, addr, mask, enable):
            self.WDATA @= data
            self.WADDR @= addr
            self.WMASK @= mask
            self.WE @= enable

        self.write = write


class Cache(m.Generator2):
    def __init__(self, x_len, n_ways: int, n_sets: int, b_bytes: int):
        b_bits = b_bytes << 3
        b_len = m.bitutils.clog2(b_bytes)
        s_len = m.bitutils.clog2(n_sets)
        t_len = x_len - (s_len + b_len)
        n_words = b_bits // x_len
        w_bytes = x_len // 8
        byte_offset_bits = m.bitutils.clog2(w_bytes)
        nasti_params = NastiParameters(data_bits=64, addr_bits=x_len,
                                       id_bits=5)
        data_beats = b_bits // nasti_params.x_data_bits

        class MetaData(m.Product):
            tag = m.UInt[t_len]

        self.io = m.IO(**make_cache_ports(x_len, nasti_params))
        self.io += m.ClockIO(has_reset=True)

        class State(m.Enum):
            IDLE = 0
            READ_CACHE = 1
            WRITE_CACHE = 2
            WRITE_BACK = 3
            WRITE_ACK = 4
            REFILL_READY = 5
            REFILL = 6

        state = m.Register(init=State.IDLE, reset_type=m.Reset)()

        # memory
        v = m.Register(m.UInt[n_sets], has_enable=True)()
        d = m.Register(m.UInt[n_sets], has_enable=True)()
        meta_mem = m.Memory(n_sets, MetaData, read_latency=1,
                            has_read_enable=True)()
        data_mem = [ArrayMaskMem(n_sets, w_bytes, m.UInt[8], read_latency=1,
                                 has_read_enable=True)()
                    for _ in range(n_words)]

        addr_reg = m.Register(type(self.io.cpu.req.data.addr).undirected_t,
                              has_enable=True)()
        cpu_data = m.Register(type(self.io.cpu.req.data.data).undirected_t,
                              has_enable=True)()
        cpu_mask = m.Register(type(self.io.cpu.req.data.mask).undirected_t,
                              has_enable=True)()

        self.io.nasti.r.ready @= state.O == State.REFILL
        # Counters
        assert data_beats > 0
        if data_beats > 1:
            read_counter = Counter(
                data_beats,
                has_enable=True,
                has_cout=True,
                reset_type=m.Reset
            )()
            read_counter.CE @= m.enable(self.io.nasti.r.fired())
            read_count, read_wrap_out = read_counter.O, read_counter.COUT

            write_counter = Counter(
                data_beats,
                has_enable=True,
                has_cout=True,
                reset_type=m.Reset
            )()
            write_count, write_wrap_out = write_counter.O, write_counter.COUT
        else:
            read_count, read_wrap_out = 0, 1
            write_count, write_wrap_out = 0, 1

        refill_buf = m.Register(
            m.Array[data_beats, m.UInt[nasti_params.x_data_bits]],
            has_enable=True
        )()
        if data_beats == 1:
            refill_buf.I[0] @= self.io.nasti.r.data.data
        else:
            refill_buf.I @= m.set_index(refill_buf.O,
                                        self.io.nasti.r.data.data,
                                        read_count)
        refill_buf.CE @= m.enable(self.io.nasti.r.fired())

        is_idle = state.O == State.IDLE
        is_read = state.O == State.READ_CACHE
        is_write = state.O == State.WRITE_CACHE
        is_alloc = (state.O == State.REFILL) & read_wrap_out
        # m.display("[%0t]: is_alloc = %x", m.time(), is_alloc)\
        #     .when(m.posedge(self.io.CLK))
        is_alloc_reg = m.Register(m.Bit)()(is_alloc)

        hit = m.Bit(name="hit")
        wen = is_write & (hit | is_alloc_reg) & ~self.io.cpu.abort | is_alloc
        # m.display("[%0t]: wen = %x", m.time(), wen)\
        #     .when(m.posedge(self.io.CLK))
        ren = m.enable(~wen & (is_idle | is_read) & self.io.cpu.req.valid)
        ren_reg = m.enable(m.Register(m.Bit)()(ren))

        addr = self.io.cpu.req.data.addr
        idx = addr[b_len:s_len + b_len]
        tag_reg = addr_reg.O[s_len + b_len:x_len]
        idx_reg = addr_reg.O[b_len:s_len + b_len]
        off_reg = addr_reg.O[byte_offset_bits:b_len]

        rmeta = meta_mem.read(idx, ren)
        rdata = m.concat(*(mem.read(idx, ren) for mem in data_mem))
        rdata_buf = m.Register(type(rdata), has_enable=True)()(rdata,
                                                               CE=ren_reg)

        read = m.mux([
            m.as_bits(m.mux([
                rdata_buf,
                rdata
            ], ren_reg)),
            m.as_bits(refill_buf.O)
        ], is_alloc_reg)
        # m.display("is_alloc_reg=%x", is_alloc_reg)\
        #     .when(m.posedge(self.io.CLK))

        hit @= v.O[idx_reg] & (rmeta.tag == tag_reg)

        # read mux
        self.io.cpu.resp.data.data @= m.array(
            [read[i * x_len:(i + 1) * x_len] for i in range(n_words)]
        )[off_reg]
        self.io.cpu.resp.valid @= (is_idle | (is_read & hit) |
                                   (is_alloc_reg & ~cpu_mask.O.reduce_or()))
        m.display("resp.valid=%x", self.io.cpu.resp.valid.value())\
            .when(m.posedge(self.io.CLK))
        m.display("[%0t]: valid = %x", m.time(),
                  self.io.cpu.resp.valid.value())\
            .when(m.posedge(self.io.CLK))
        m.display("[%0t]: is_idle = %x, is_read = %x, hit = %x, is_alloc_reg = "
                  "%x, ~cpu_mask.O.reduce_or() = %x", m.time(), is_idle,
                  is_read, hit, is_alloc_reg, ~cpu_mask.O.reduce_or())\
            .when(m.posedge(self.io.CLK))
        m.display("[%0t]: refill_buf.O=%x, %x", m.time(), *refill_buf.O)\
            .when(m.posedge(self.io.CLK))\
            .if_(self.io.cpu.resp.valid.value() & is_alloc_reg)
        m.display("[%0t]: read=%x", m.time(), read)\
            .when(m.posedge(self.io.CLK))\
            .if_(self.io.cpu.resp.valid.value() & is_alloc_reg)

        addr_reg.I @= addr
        addr_reg.CE @= m.enable(self.io.cpu.resp.valid.value())

        cpu_data.I @= self.io.cpu.req.data.data
        cpu_data.CE @= m.enable(self.io.cpu.resp.valid.value())

        cpu_mask.I @= self.io.cpu.req.data.mask
        cpu_mask.CE @= m.enable(self.io.cpu.resp.valid.value())

        wmeta = MetaData(name="wmeta")
        wmeta.tag @= tag_reg

        offset_mask = (
            m.zext_to(cpu_mask.O, w_bytes * 8) <<
            m.zext_to(
                m.concat(m.bits(0, byte_offset_bits), off_reg),
                w_bytes * 8
            )
        )
        wmask = m.mux([
            m.SInt[w_bytes * 8](-1),
            m.sint(offset_mask)
        ], ~is_alloc)

        if len(refill_buf.O) == 1:
            wdata_alloc = self.io.nasti.r.data.data
        else:
            wdata_alloc = m.concat(
                # TODO: not sure why they use `init.reverse`
                # https://github.com/ucb-bar/riscv-mini/blob/release/src/main/scala/Cache.scala#L116
                m.concat(*refill_buf.O[:-1]),
                self.io.nasti.r.data.data
            )
        wdata = m.mux([
            wdata_alloc,
            m.as_bits(m.repeat(cpu_data.O, n_words))
        ], ~is_alloc)

        v.I @= m.set_index(v.O, m.bit(True), idx_reg)
        v.CE @= m.enable(wen)
        d.I @= m.set_index(d.O, ~is_alloc, idx_reg)
        d.CE @= m.enable(wen)
        # m.display("[%0t]: refill_buf.O = %x", m.time(),
        #           m.concat(*refill_buf.O)).when(m.posedge(self.io.CLK)).if_(wen)
        # m.display("[%0t]: nasti.r.data.data = %x", m.time(),
        #           self.io.nasti.r.data.data).when(m.posedge(self.io.CLK)).if_(wen)

        meta_mem.write(wmeta, idx_reg, m.enable(wen & is_alloc))
        for i, mem in enumerate(data_mem):
            data = [wdata[i * x_len + j * 8:i * x_len + (j + 1) * 8]
                    for j in range(w_bytes)]
            mem.write(m.array(data), idx_reg,
                      wmask[i * w_bytes: (i + 1) * w_bytes], m.enable(wen))
            # m.display("[%0t]: wdata = %x, %x, %x, %x", m.time(),
            #           *mem.WDATA.value()).when(m.posedge(self.io.CLK)).if_(wen)
            # m.display("[%0t]: wmask = %x, %x, %x, %x", m.time(),
            #           *mem.WMASK.value()).when(m.posedge(self.io.CLK)).if_(wen)

        tag_and_idx = m.zext_to(m.concat(idx_reg, tag_reg),
                                nasti_params.x_addr_bits)
        self.io.nasti.ar.data @= NastiReadAddressChannel(
            nasti_params, 0, tag_and_idx << m.Bits[len(tag_and_idx)](b_len),
            m.bitutils.clog2(nasti_params.x_data_bits // 8), data_beats - 1)

        rmeta_and_idx = m.zext_to(m.concat(idx_reg, rmeta.tag),
                                  nasti_params.x_addr_bits)
        self.io.nasti.aw.data @= NastiWriteAddressChannel(
            nasti_params, 0, rmeta_and_idx <<
            m.Bits[len(rmeta_and_idx)](b_len),
            m.bitutils.clog2(nasti_params.x_data_bits // 8), data_beats - 1)

        self.io.nasti.w.data @= NastiWriteDataChannel(
            nasti_params,
            m.array(
                [read[i * nasti_params.x_data_bits:
                      (i + 1) * nasti_params.x_data_bits]
                 for i in range(data_beats)]
            )[write_count],
            None, write_wrap_out
        )

        is_dirty = v.O[idx_reg] & d.O[idx_reg]

        # TODO: Have to use temporary so we can invoke `fired()`
        aw_valid = m.Bit(name="aw_valid")
        self.io.nasti.aw.valid @= aw_valid

        ar_valid = m.Bit(name="ar_valid")
        self.io.nasti.ar.valid @= ar_valid

        b_ready = m.Bit(name="b_ready")
        self.io.nasti.b.ready @= b_ready

        state.I @= state.O
        aw_valid @= False
        ar_valid @= False
        self.io.nasti.w.valid @= False
        b_ready @= False
        with m.when(state.O == State.IDLE):
            with m.when(self.io.cpu.req.valid):
                with m.when(self.io.cpu.req.data.mask.reduce_or()):
                    state.I @= State.WRITE_CACHE
                with m.otherwise():
                    state.I @= State.READ_CACHE
        with m.elsewhen(state.O == State.READ_CACHE):
            with m.when(hit):
                with m.when(self.io.cpu.req.valid):
                    with m.when(self.io.cpu.req.data.mask.reduce_or()):
                        state.I @= State.WRITE_CACHE
                    with m.otherwise():
                        state.I @= State.READ_CACHE
                with m.otherwise():
                    state.I @= State.IDLE
            with m.otherwise():
                aw_valid @= is_dirty
                ar_valid @= ~is_dirty
                with m.when(self.io.nasti.aw.fired()):
                    state.I @= State.WRITE_BACK
                with m.elsewhen(self.io.nasti.ar.fired()):
                    state.I @= State.REFILL
        with m.elsewhen(state.O == State.WRITE_CACHE):
            with m.when(hit | is_alloc_reg | self.io.cpu.abort):
                state.I @= State.IDLE
            with m.otherwise():
                aw_valid @= is_dirty
                ar_valid @= ~is_dirty
                with m.when(self.io.nasti.aw.fired()):
                    state.I @= State.WRITE_BACK
                with m.elsewhen(self.io.nasti.ar.fired()):
                    state.I @= State.REFILL
        with m.elsewhen(state.O == State.WRITE_BACK):
            self.io.nasti.w.valid @= True
            with m.when(write_wrap_out):
                state.I @= State.WRITE_ACK
        with m.elsewhen(state.O == State.WRITE_ACK):
            b_ready @= True
            with m.when(self.io.nasti.b.fired()):
                state.I @= State.REFILL_READY
        with m.elsewhen(state.O == State.REFILL_READY):
            ar_valid @= True
            with m.when(self.io.nasti.ar.fired()):
                state.I @= State.REFILL
        with m.elsewhen(state.O == State.REFILL):
            with m.when(read_wrap_out):
                with m.when(cpu_mask.O.reduce_or()):
                    state.I @= State.WRITE_CACHE
                with m.otherwise():
                    state.I @= State.IDLE

        if data_beats > 1:
            # TODO: Have to do this at the end since the inline comb logic
            # wires up nasti.w
            write_counter.CE @= m.enable(self.io.nasti.w.fired())
