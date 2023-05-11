import magma as m
from collections import namedtuple


class NastiParameters:
    def __init__(self, data_bits, addr_bits, id_bits):
        self.data_bits = data_bits
        self.addr_bits = addr_bits
        self.id_bits = id_bits
        self.x_data_bits = self.data_bits
        self.w_strobe_bits = self.data_bits // 8
        self.x_addr_bits = self.addr_bits
        self.w_id_bits = self.id_bits
        self.r_id_bits = self.id_bits
        self.x_id_bits = self.id_bits
        self.x_user_bits = 1
        self.a_w_user_bits = self.x_user_bits
        self.w_user_bits = self.x_user_bits
        self.b_user_bits = self.x_user_bits
        self.a_r_user_bits = self.x_user_bits
        self.r_user_bits = self.x_user_bits
        self.x_len_bits = 8
        self.x_size_bits = 3
        self.x_burst_bits = 2
        self.x_cache_bits = 4
        self.x_prot_bits = 3
        self.x_qos_bits = 4
        self.x_region_bits = 4
        self.x_resp_bits = 2

    def bytes_to_x_size(self, bytes_):
        return m.dict_lookup({
            1: m.bits(0, 3),
            2: m.bits(1, 3),
            4: m.bits(2, 3),
            8: m.bits(3, 3),
            16: m.bits(4, 3),
            32: m.bits(5, 3),
            64: m.bits(6, 3),
            128: m.bits(7, 3),
        }, bytes_, m.bits(0b111, 3))


def make_NastiMetadataIO(nasti_params):
    class NastiMetadataIO(m.Product):
        addr = m.UInt[nasti_params.x_addr_bits]
        length = m.UInt[nasti_params.x_len_bits]
        size = m.UInt[nasti_params.x_size_bits]
        burst = m.UInt[nasti_params.x_burts_bits]
        lock = m.Bit
        cache = m.UInt[nasti_params.x_cache_bits]
        prot = m.UInt[nasti_params.x_prot_bits]
        qos = m.UInt[nasti_params.x_qos_bits]
        region = m.UInt[nasti_params.x_region_bits]
    return NastiMetadataIO


def make_NastiDataIO(nasti_params):
    class NastiDataIO(m.Product):
        data = m.UInt(nasti_params.x_data_bits)
        last = m.Bit
    return NastiDataIO


class NastiMasterToSlaveChannel(m.Product):
    pass


class NastiSlaveToMasterChannel(m.Product):
    pass


class NastiAddressChannel(NastiMasterToSlaveChannel):
    pass


# TODO: Use inheritance pattern when available
# def make_NastiResponseChannel(nasti_params):
#     class NastiResponseChannel(NastiSlaveToMasterChannel):
#         resp = m.UInt[nasti_params.x_resp_bits]
#     return NastiResponseChannel


def make_NastiWriteAddressChannel(nasti_params):
    class NastiWriteAddressChannel(NastiAddressChannel):
        id = m.UInt[nasti_params.w_id_bits]
        user = m.UInt[nasti_params.a_w_user_bits]

        # metadata/address channel common
        addr = m.UInt[nasti_params.x_addr_bits]
        length = m.UInt[nasti_params.x_len_bits]
        size = m.UInt[nasti_params.x_size_bits]
        burst = m.UInt[nasti_params.x_burst_bits]
        lock = m.Bit
        cache = m.UInt[nasti_params.x_cache_bits]
        prot = m.UInt[nasti_params.x_prot_bits]
        qos = m.UInt[nasti_params.x_qos_bits]
        region = m.UInt[nasti_params.x_region_bits]
    return NastiWriteAddressChannel


def make_NastiWriteDataChannel(nasti_params):
    class NastiWriteDataChannel(NastiSlaveToMasterChannel):
        id = m.UInt[nasti_params.w_id_bits]
        strb = m.UInt[nasti_params.w_strobe_bits]
        user = m.UInt[nasti_params.w_user_bits]
        data = m.UInt[nasti_params.x_data_bits]
        last = m.Bit
    return NastiWriteDataChannel


def make_NastiWriteResponseChannel(nasti_params):
    class NastiWriteResponseChannel(NastiSlaveToMasterChannel):
        resp = m.UInt[nasti_params.x_resp_bits]
        id = m.UInt[nasti_params.w_id_bits]
        user = m.UInt[nasti_params.b_user_bits]
    return NastiWriteResponseChannel


def make_NastiReadAddressChannel(nasti_params):
    class NastiReadAddressChannel(NastiAddressChannel):
        id = m.UInt[nasti_params.r_id_bits]
        user = m.UInt[nasti_params.a_r_user_bits]

        # metadata/address channel common
        addr = m.UInt[nasti_params.x_addr_bits]
        length = m.UInt[nasti_params.x_len_bits]
        size = m.UInt[nasti_params.x_size_bits]
        burst = m.UInt[nasti_params.x_burst_bits]
        lock = m.Bit
        cache = m.UInt[nasti_params.x_cache_bits]
        prot = m.UInt[nasti_params.x_prot_bits]
        qos = m.UInt[nasti_params.x_qos_bits]
        region = m.UInt[nasti_params.x_region_bits]
    return NastiReadAddressChannel


def make_NastiReadDataChannel(nasti_params):
    class NastiReadDataChannel(NastiSlaveToMasterChannel):
        resp = m.UInt[nasti_params.x_resp_bits]
        id = m.UInt[nasti_params.r_id_bits]
        user = m.UInt[nasti_params.r_user_bits]
        data = m.UInt[nasti_params.x_data_bits]
        last = m.Bit
    return NastiReadDataChannel


def make_NastiReadIO(nasti_params):
    class NastiReadIO(m.Product):
        ar = m.Producer(
            m.Decoupled[make_NastiReadAddressChannel(nasti_params)]
        )
        r = m.Consumer(m.Decoupled[make_NastiReadDataChannel(nasti_params)])

    return NastiReadIO


def make_NastiWriteIO(nasti_params):
    class NastiWriteIO(m.Product):
        aw = m.Producer(
            m.Decoupled[make_NastiWriteAddressChannel(nasti_params)]
        )
        w = m.Producer(m.Decoupled[make_NastiWriteDataChannel(nasti_params)])
        b = m.Consumer(
            m.Decoupled[make_NastiWriteResponseChannel(nasti_params)]
        )
    return NastiWriteIO


def make_NastiIO(nasti_params):
    class NastiIO(m.Product):
        aw = m.Producer(
            m.Decoupled[make_NastiWriteAddressChannel(nasti_params)]
        )
        w = m.Producer(m.Decoupled[make_NastiWriteDataChannel(nasti_params)])
        b = m.Consumer(
            m.Decoupled[make_NastiWriteResponseChannel(nasti_params)]
        )

        ar = m.Producer(
            m.Decoupled[make_NastiReadAddressChannel(nasti_params)]
        )
        r = m.Consumer(m.Decoupled[make_NastiReadDataChannel(nasti_params)])
    return NastiIO


class NastiConstants:
    BURST_FIXED = m.UInt[2](0b00)
    BURST_INCR = m.UInt[2](0b01)
    BURST_WRAP = m.UInt[2](0b10)

    RESP_OKAY = m.UInt[2](0b00)
    RESP_EXOKAY = m.UInt[2](0b01)
    RESP_SLVERR = m.UInt[2](0b10)
    RESP_DECERR = m.UInt[2](0b11)

    CACHE_DEVICE_NOBUF = m.UInt[4](0b0000)
    CACHE_DEVICE_BUF = m.UInt[4](0b0001)
    CACHE_NORMAL_NOCACHE_NOBUF = m.UInt[4](0b0010)
    CACHE_NORMAL_NOCACHE_BUF = m.UInt[4](0b0011)

    def AXPROT(instruction, nonsecure, privileged):
        assert isinstance(instruction, m.Bit)
        assert isinstance(nonsecure, m.Bit)
        assert isinstance(privileged, m.Bit)
        return m.bits([instruction, nonsecure, privileged])


def NastiWriteAddressChannel(nasti_params, id, addr, size, length=0,
                             burst=NastiConstants.BURST_INCR):
    aw = make_NastiWriteAddressChannel(nasti_params)()
    aw.id @= id
    aw.addr @= addr
    aw.length @= length
    aw.size @= size
    aw.burst @= burst
    aw.lock @= m.Bit(0)
    aw.cache @= NastiConstants.CACHE_DEVICE_NOBUF
    aw.prot @= NastiConstants.AXPROT(m.bit(0), m.bit(0), m.bit(0))
    aw.qos @= m.UInt[4](0b0000)
    aw.region @= m.UInt[4](0b0000)
    aw.user @= 0
    return aw


def NastiReadAddressChannel(nasti_params, id, addr, size, length=0,
                            burst=NastiConstants.BURST_INCR):
    ar = make_NastiReadAddressChannel(nasti_params)()
    ar.id @= id
    ar.addr @= addr
    ar.length @= length
    ar.size @= size
    ar.burst @= burst
    ar.lock @= m.Bit(0)
    ar.cache @= NastiConstants.CACHE_DEVICE_NOBUF
    ar.prot @= NastiConstants.AXPROT(m.bit(0), m.bit(0), m.bit(0))
    ar.qos @= m.UInt[4](0b0000)
    ar.region @= m.UInt[4](0b0000)
    ar.user @= 0
    return ar


def NastiWriteDataChannel(nasti_params, data, strb=None, last=True, id=0):
    w = make_NastiWriteDataChannel(nasti_params)()
    if strb is None:
        strb = m.repeat(1, nasti_params.w_strobe_bits)
    w.strb @= strb
    w.data @= data
    w.last @= last
    w.id @= id
    w.user @= 0
    return w


def NastiReadDataChannel(nasti_params, id, data, last=True, resp=0):
    r = make_NastiReadDataChannel(nasti_params)()
    r.id @= id
    r.data @= data
    r.last @= last
    r.resp @= resp
    r.user @= 0
    return r


def NastiWriteResponseChannel(nasti_params, id, resp=0):
    b = make_NastiWriteResponseChannel(nasti_params)()
    b.id @= id
    b.resp @= resp
    b.user @= 0
    return b
