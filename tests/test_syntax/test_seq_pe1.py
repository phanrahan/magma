import magma as m
from peak import Peak

Bit = m.Bit
Bits = m.Bits
Product = m.Tuple

DATAWIDTH = 16
Data = Bits(DATAWIDTH)


LUT = Bits(8)


# class Cond(m.Enum):
Cond = m.Enum(
    Z=0,    # EQ
    Z_n=1,  # NE
    C=2,    # UGE
    C_n=3,  # ULT
    N=4,    # <  0
    N_n=5,  # >= 0
    V=6,    # Overflow
    V_n=7,  # No overflow
    EQ=0,
    NE=1,
    UGE=2,
    ULT=3,
    UGT=8,
    ULE=9,
    SGE=10,
    SLT=11,
    SGT=12,
    SLE=13,
    LUT=14,
    ALU=15
)


# class Mode(m.Enum):
Mode = m.Enum(
    CONST=0,  # Register returns constant in constant field
    VALID=1,  # Register written with clock enable, previous value returned
    BYPASS=2,  # Register is bypassed and input value is returned
    DELAY=3  # Register written with input value, previous value returned
)


# Constant values for registers
RegA_Const = Bits(DATAWIDTH)
RegB_Const = Bits(DATAWIDTH)
RegD_Const = Bits(1)
RegE_Const = Bits(1)
RegF_Const = Bits(1)

# Modes for registers
RegA_Mode = Mode
RegB_Mode = Mode
RegD_Mode = Mode
RegE_Mode = Mode
RegF_Mode = Mode

# ALU operations
# class ALU(Enum):
ALU = m.Enum(
    Add=0,
    Sub=1,
    Abs=3,
    GTE_Max=4,
    LTE_Min=5,
    Sel=8,
    Mult0=0xb,
    Mult1=0xc,
    Mult2=0xd,
    SHR=0xf,
    SHL=0x11,
    Or=0x12,
    And=0x13,
    XOr=0x14
)

# Whether the operation is unsigned (0) or signed (1)
Signed = Bits(1)


# class Inst(Product):
Inst = Product(
    alu=ALU,  # ALU operation
    signed=Signed,  # unsigned or signed
    lut=LUT,  # LUT operation as a 3-bit LUT
    cond=Cond,  # Condition code (see cond.py)
    rega=RegA_Mode,  # RegA mode (see mode.py)
    data0=RegA_Const,  # RegA constant (16-bits)
    regb=RegB_Mode,  # RegB mode
    data1=RegB_Const,  # RegB constant (16-bits)
    regd=RegD_Mode,  # RegD mode
    bit0=RegD_Const,  # RegD constant (1-bit)
    rege=RegE_Mode,  # RegE mode
    bit1=RegE_Const,  # RegE constant (1-bit)
    regf=RegF_Mode,  # RegF mode
    bit2=RegF_Const    # RegF constant (1-bit)
)


#
# Implement condition code logic
#
# Inputs are the condition code field, the alu result, the lut result,
# and the flags Z, N, C, V
#
def cond(code: Cond, alu: Bit, lut: Bit, Z: Bit, N: Bit, C: Bit,
         V: Bit) -> Bit:
    if code == Cond.Z:
        return Z
    elif code == Cond.Z_n:
        return not Z
    elif code == Cond.C or code == Cond.UGE:
        return C
    elif code == Cond.C_n or code == Cond.ULT:
        return not C
    elif code == Cond.N:
        return N
    elif code == Cond.N_n:
        return not N
    elif code == Cond.V:
        return V
    elif code == Cond.V_n:
        return not V
    elif code == Cond.UGT:
        return C and not Z
    elif code == Cond.ULE:
        return not C or Z
    elif code == Cond.SGE:
        return N == V
    elif code == Cond.SLT:
        return N != V
    elif code == Cond.SGT:
        return not Z and (N == V)
    elif code == Cond.SLE:
        return Z or (N != V)
    elif code == Cond.ALU:
        return alu
    elif code == Cond.LUT:
        return lut
    raise NotImplementedError(code)


# Implement a 3-bit LUT
def lut(lut: LUT, bit0: Bit, bit1: Bit, bit2: Bit) -> Bit:
    i = (int(bit2) << 2) | (int(bit1) << 1) | int(bit0)
    return Bit(lut & (1 << i))


def DefineRegister(width, init=0):
    @m.circuit.sequential
    class Register(Peak):
        def __init__(self):
            self.value: Bits(width) = m.bits(init, width)

        def __call__(self, value: Bits(width), en: Bit) -> Bits(width):
            retvalue = self.value
            if en:
                self.value = value
            return retvalue

    return Register


def DefineRegisterMode(width, init=0):
    @m.circuit.sequential
    class RegisterMode(Peak):
        def __init__(self):
            # TODO: Changed register to be implicit
            self.register: Bits(width) = [DefineRegister(width, init)()]

        def __call__(self, mode: Mode, const: Bits(width), value: Bits(width),
                     clk_en: Bit) -> Bits(width):
            if mode == Mode.CONST:
                self.register(value, m.bit(False))
                return const
            elif mode == Mode.BYPASS:
                self.register(value, m.bit(False))
                return value
            elif mode == Mode.DELAY:
                # return self.register(value, True)
                return self.register(value, m.bit(True))
            elif mode == Mode.VALID:
                return self.register(value, clk_en)
    return RegisterMode


@m.circuit.combinational
def alu(alu: ALU, signed: Signed, a: Data, b: Data, d: Bit) -> (Data, Bit):
    if signed:
        a = m.sint(a)
        b = m.sint(b)
        # mula, mulb = a.sext(16), b.sext(16)
        mula, mulb = m.sext(a, 8), m.sext(b, 8)
        mul = mula * mulb
    else:
        # mula, mulb = a.zext(16), b.zext(16)
        a = m.uint(a)
        b = m.uint(b)
        mula, mulb = m.zext(a, 8), m.zext(b, 8)
        mul = mula * mulb
    # Had to move up because of polymorphism issue
    # mul = mula * mulb

    C = 0
    V = 0
    if alu == ALU.Add:
        res, C = a.adc(b, Bit(0))
        V = overflow(a, b, res)
        res_p = C
    elif alu == ALU.Sub:
        b_not = ~b
        res, C = a.adc(b_not, Bit(1))
        V = overflow(a, b_not, res)
        res_p = C
    elif alu == ALU.Mult0:
        res, C, V = mul[:16], 0, 0  # wrong C, V
        res_p = C
    elif alu == ALU.Mult1:
        res, C, V = mul[8:24], 0, 0  # wrong C, V
        res_p = C
    elif alu == ALU.Mult2:
        res, C, V = mul[16:32], 0, 0  # wrong C, V
        res_p = C
    elif alu == ALU.GTE_Max:
        # C, V = a-b?
        pred = a >= b
        res, res_p = pred.ite(a, b), a >= b
    elif alu == ALU.LTE_Min:
        # C, V = a-b?
        pred = a <= b
        res, res_p = pred.ite(a, b), a >= b
    elif alu == ALU.Abs:
        pred = a >= 0
        res, res_p = pred.ite(a, -a), Bit(a[-1])
    elif alu == ALU.Sel:
        res, res_p = d.ite(a, b), 0
    elif alu == ALU.And:
        res, res_p = a & b, 0
    elif alu == ALU.Or:
        res, res_p = a | b, 0
    elif alu == ALU.XOr:
        res, res_p = a ^ b, 0
    elif alu == ALU.SHR:
        res, res_p = a >> b[:4], 0
    elif alu == ALU.SHL:
        res, res_p = a << b[:4], 0
    elif alu == ALU.Neg:
        if signed:
            res, res_p = ~a + Bit(1), 0
        else:
            res, res_p = ~a, 0
    else:
        raise NotImplementedError(alu)

    Z = res == 0
    N = Bit(res[-1])

    return res, res_p, Z, N, C, V


@m.circuit.sequential
class PE:
    def __init__(self):
        # Declare PE state

        # Data registers
        # self.rega = RegisterMode(Data)
        # self.regb = RegisterMode(Data)

        # Bit Registers
        # self.regd = RegisterMode(Bit)
        # self.rege = RegisterMode(Bit)
        # self.regf = RegisterMode(Bit)

        self.rega: Data = [DefineRegisterMode(DATAWIDTH)()]
        self.regb: Data = [DefineRegisterMode(DATAWIDTH)()]

        # Bit Registers
        self.regd: Bit = [DefineRegisterMode(1)()]
        self.rege: Bit = [DefineRegisterMode(1)()]
        self.regf: Bit = [DefineRegisterMode(1)()]

    # @name_outputs(alu_res=Data, res_p=Bit, irq=Bit)
    # def __call__(self, inst: Inst,
    #              data0: Data, data1: Data = Data(0),
    #              bit0: Bit = Bit(0), bit1: Bit = Bit(0), bit2: Bit = Bit(0),
    #              clk_en: Bit = Bit(1)):
    def __call__(self, inst: Inst,
                 data0: Data, data1: Data,
                 bit0: Bit, bit1: Bit, bit2: Bit,
                 clk_en: Bit) -> Product(Data, Bit, Bit):

        # Simulate one clock cycle

        ra = self.rega(inst.rega, inst.data0, data0, clk_en)
        rb = self.regb(inst.regb, inst.data1, data1, clk_en)

        rd = self.regd(inst.regd, inst.bit0, bit0, clk_en)
        re = self.rege(inst.rege, inst.bit1, bit1, clk_en)
        rf = self.regf(inst.regf, inst.bit2, bit2, clk_en)

        # calculate alu results
        alu_res, alu_res_p, Z, N, C, V = alu(inst.alu, inst.signed, ra, rb, rd)

        # calculate lut results
        lut_res = lut(inst.lut, rd, re, rf)

        # calculate 1-bit result
        res_p = cond(inst.cond, alu_res, lut_res, Z, N, C, V)

        # calculate interrupt request
        irq = Bit(0)  # NYI

        # return 16-bit result, 1-bit result, irq
        return alu_res, res_p, irq
