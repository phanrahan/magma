from magma import cache_definition
from magma.t import Type
from magma.bit import Bit, BitType, In, Out
from magma.clock import Clock
from magma.bits import Bits, BitsType, SInt, SIntType, UInt, UIntType
from magma.circuit import DeclareCircuit, circuit_type_method, DefineCircuit, EndDefine
from magma.compatibility import IntegerTypes
from magma.bit_vector import BitVector
from magma.wire import wire
from magma.conversions import array, bits, uint, sint
import operator
import math
from functools import wraps, reduce
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

__all__  = ['DefineMux']
__all__ += ['DefineRegister']
__all__ += ['DefineMemory']
__all__ += ['DefineAnd', 'And', 'and_']
__all__ += ['DefineOr', 'Or', 'or_']
__all__ += ['DefineXOr', 'XOr', 'xor']
__all__ += ['DefineInvert', 'Invert', 'invert']
__all__ += ['DefineEQ', 'EQ', 'eq'] 
# __all__ += ['DefineNE', 'NE', 'ne']

__all__ += ['lshift', 'rshift']
__all__ += ['add', 'sub', "mul", "div", "truediv"]
__all__ += ['lt', 'le', "gt", "ge"]
__all__ += ['concat', 'repeat']
__all__ += ['zext', 'sext']


def type_check_definition_params(fn):
    @wraps(fn)
    def wrapped(height=2, width=None):
        if not isinstance(height, IntegerTypes) or height < 2:
            raise ValueError("Height must be an integer greater than or equal "
                    "to 2, not {}".format(height))
        if width is not None and (not isinstance(width, IntegerTypes) or width < 1):
            raise ValueError("Width must be None or an integer greater than or"
                    " equal to 1, not {}".format(height))
        return fn(height, width)
    return wrapped


def type_check_binary_operator(operator):
    """
    For binary operations, the other argument must be the same type or a list
    of bits of the same length
    """
    def type_checked_operator(self, other):
        if not (isinstance(other, list) and len(self) == len(other)) and \
           type(self) != type(other):
            raise TypeError("unsupported operand type(s) for {}: '{}' and"
                            "'{}'".format(operator.__name__, type(self),
                                          type(other)))
        return operator(self, other)
    return type_checked_operator


def declare_bit_binop(name, op, python_op, firrtl_op):
    def simulate(self, value_store, state_store):
        in0 = BitVector(value_store.get_value(self.in0))
        in1 = BitVector(value_store.get_value(self.in1))
        out = python_op(in0, in1).as_bool_list()[0]
        value_store.set_value(self.out, out)

    circ = DeclareCircuit("{}".format(name),
                          'in0', In(Bit), 'in1', In(Bit), 'out', Out(Bit),
                          simulate=simulate,
                          firrtl_op=firrtl_op)

    @type_check_binary_operator
    def func(self, other):
        return circ()(self, other)
    func.__name__ = op
    setattr(BitType, op, func)

    return circ


# And should decide to call BitAnd vs And ...
BitAnd = declare_bit_binop("coreir_bitand", "__and__", operator.and_, "and")
BitOr  = declare_bit_binop("coreir_bitor", "__or__", operator.or_, "or")
BitXOr = declare_bit_binop("coreir_bitxor", "__xor__", operator.xor, "xor")

def simulate_bit_not(self, value_store, state_store):
    _in = BitVector(value_store.get_value(getattr(self, "in")))
    out = (~_in).as_bool_list()[0]
    value_store.set_value(self.out, out)


DefineCoreirNot = DeclareCircuit("coreir_bitnot", 'in', In(Bit), 'out', Out(Bit),
    simulate=simulate_bit_not)

def DefineNot(width=None):
    if width != None:
        raise ValueError("Not is only defined as a 1-bit operation, width must"
                " be None")
    return DefineCoreirNot

def Not():
    def not_generator(arg):
        assert isinstance(arg, BitType)
        return DefineNot()()(arg)
    return not_generator


def not_(self):
    return Not()(self)


BitType.__invert__ = not_


def declare_bits_binop(name, op, python_op):
    def simulate(self, value_store, state_store):
        in0 = BitVector(value_store.get_value(self.in0))
        in1 = BitVector(value_store.get_value(self.in1))
        out = python_op(in0, in1).as_bool_list()
        value_store.set_value(self.out, out)

    @cache_definition
    def Declare(N):
        T = Bits(N)
        return DeclareCircuit("{}{}".format(name, N),
                              'in0', In(T), 'in1', In(T), 'out', Out(T),
                              simulate=simulate,
                              verilog_name=name,
                              default_kwargs={"width": N})

    @type_check_binary_operator
    def func(self, other):
        return Declare(self.N)()(self, other)
    func.__name__ = op
    setattr(BitsType, op, func)
    return Declare


@cache_definition
def DefineFoldOp(DefineOp, op, height, width):
    T = Bits(width)
    IO = []
    for i in range(height):
        IO += ["I{}".format(i), In(T)]
    IO += ["O", Out(T)]
    circ = DefineCircuit("fold_{}{}{}".format(op, height, width), *IO)
    reduce_args = [getattr(circ, "I{}".format(i)) for i in range(height)]
    Op2 = DefineOp(2, width)
    wire(reduce(lambda x, y: Op2()(x, y), reduce_args), circ.O)
    EndDefine()
    return circ


DefineCoreirAnd = declare_bits_binop("coreir_and", "__and__", operator.and_)

@type_check_definition_params
def DefineAnd(height=2, width=None):
    if width is None:
        return BitAnd
    elif height is 2:
        return DefineCoreirAnd(width)
    else:
        return DefineFoldOp(DefineAnd, "and", height, width)


def And(height, **kwargs):
    def AndGenerator(*args):
        if all(isinstance(arg, BitType) for arg in args):
            width = None
        else:
            assert all(isinstance(arg, BitsType) for arg in args)
            width = len(args[0])
            assert all(len(arg) == width for arg in args)
        return DefineAnd(height, width)(**kwargs)(*args)
    return AndGenerator


def and_(*args):
    return And(len(args))(*args)


DefineCoreirOr  = declare_bits_binop("coreir_or", "__or__", operator.or_)

@type_check_definition_params
def DefineOr(height=2, width=None):
    if width is None:
        return BitOr
    elif height is 2:
        return DefineCoreirOr(width)
    else:
        return DefineFoldOp(DefineOr, "or", height, width)


def Or(height, **kwargs):
    def OrGenerator(*args):
        if all(isinstance(arg, BitType) for arg in args):
            width = None
        else:
            assert all(isinstance(arg, BitsType) for arg in args)
            width = len(args[0])
            assert all(len(arg) == width for arg in args)
        return DefineOr(height, width)(**kwargs)(*args)
    return OrGenerator


def or_(*args):
    return Or(len(args))(*args)

DefineCoreirXOr = declare_bits_binop("coreir_xor", "__xor__", operator.xor)

@type_check_definition_params
def DefineXOr(height=2, width=None):
    if width is None:
        return BitXOr
    elif height is 2:
        return DefineCoreirXOr(width)
    else:
        return DefineFoldOp(DefineXOr, "xor", height, width)


def XOr(height, **kwargs):
    def XOrGenerator(*args):
        if all(isinstance(arg, BitType) for arg in args):
            width = None
        else:
            assert all(isinstance(arg, BitsType) for arg in args)
            width = len(args[0])
            assert all(len(arg) == width for arg in args)
        return DefineXOr(height, width)(**kwargs)(*args)
    return XOrGenerator


def xor(*args):
    return XOr(len(args))(*args)


def simulate_bits_invert(self, value_store, state_store):
    _in = BitVector(value_store.get_value(getattr(self, "in")))
    out = (~_in).as_bool_list()
    value_store.set_value(self.out, out)

@cache_definition
def DefineInvert(N):
    T = Bits(N)
    return DeclareCircuit("coreir_not{}".format(N), 'in', In(T), 'out', Out(T),
            simulate=simulate_bits_invert, verilog_name="coreir_not",
            default_kwargs={"width": N})

def Invert():
    def invert_generator(arg):
        assert not isinstance(arg, BitType), "Invert not defined to Bit, use Not()"
        assert isinstance(arg, BitsType)
        return DefineInvert(len(arg))()(arg)
    return invert_generator


def invert(arg):
    return Invert()(arg)


def __invert__(self):
    return DefineInvert(self.N)()(self)

BitsType.__invert__ = __invert__


def __lshift__(self, other):
    N = self.N
    T = Bits(N)
    if isinstance(other, IntegerTypes):
        if other < 0:
            raise ValueError("Second argument to << must be positive, not "
                    "{}".format(other))

        def simulate_shift_left(self, value_store, state_store):
            _in = BitVector(value_store.get_value(getattr(self, "in")))
            out = _in << other
            value_store.set_value(self.out, out.as_bool_list())

        circ = DeclareCircuit("coreir_shl{}".format(N), 'in', In(UInt(N)),
                'out', Out(T), verilog_name="coreir_shl",
                simulate=simulate_shift_left)
        return circ(width=N, SHIFTBITS=other)(self)
    elif isinstance(other, Type):
        if not isinstance(other, UIntType):
            raise TypeError("Second argument to << must be a UInt, not "
                    "{}".format(type(other)))
        def simulate(self, value_store, state_store):
            in0 = BitVector(value_store.get_value(self.in0))
            in1 = BitVector(value_store.get_value(self.in1))
            out = (in0 << in1).as_bool_list()
            value_store.set_value(self.out, out)

        circ = DeclareCircuit("coreir_dshl{}".format(N), 'in0', In(T), 'in1',
                In(UInt(N)), 'out', Out(T), verilog_name="coreir_dshl",
                simulate=simulate)
        return circ(width=N)(self, other)
    else:
        raise TypeError("<< not implemented for argument 2 of type {}".format(
            type(other)))


BitsType.__lshift__ = __lshift__

def __rshift__(self, other):
    N = self.N
    T = Bits(N)
    if isinstance(other, IntegerTypes):
        if other < 0:
            raise ValueError("Second argument to >> must be positive, not "
                    "{}".format(other))

        def simulate_shift_left(self, value_store, state_store):
            _in = BitVector(value_store.get_value(getattr(self, "in")))
            out = _in >> other
            value_store.set_value(self.out, out.as_bool_list())

        circ = DeclareCircuit("coreir_lshr{}".format(N), 'in', In(UInt(N)),
                'out', Out(T), verilog_name="coreir_lshr",
                simulate=simulate_shift_left)
        return circ(width=N, SHIFTBITS=other)(self)
    elif isinstance(other, Type):
        if not isinstance(other, UIntType):
            raise TypeError("Second argument to >> must be a UInt, not "
                    "{}".format(type(other)))
        def simulate(self, value_store, state_store):
            in0 = BitVector(value_store.get_value(self.in0))
            in1 = BitVector(value_store.get_value(self.in1))
            out = (in0 >> in1).as_bool_list()
            value_store.set_value(self.out, out)

        circ = DeclareCircuit("coreir_dlshr{}".format(N), 'in0', In(T), 'in1',
                In(UInt(N)), 'out', Out(T), verilog_name="coreir_dlshr",
                simulate=simulate)
        return circ(width=N)(self, other)
    else:
        raise TypeError(">> not implemented for argument 2 of type {}".format(
            type(other)))


BitsType.__rshift__ = __rshift__


def declare_binop(name, _type, type_type, op, python_op, out_type=None):
    signed = type_type is SIntType
    def simulate(self, value_store, state_store):
        in0 = BitVector(value_store.get_value(self.in0), signed=signed)
        in1 = BitVector(value_store.get_value(self.in1), signed=signed)
        out = python_op(in0, in1).as_bool_list()
        if out_type is Bit:
            assert len(out) == 1, "out_type is Bit but the operation returned a list of length {}".format(len(out))
            out = out[0]
        value_store.set_value(self.out, out)

    @cache_definition
    def Declare(N):
        T = _type(N)
        return DeclareCircuit("{}{}".format(name, N),
                              'in0', In(T), 'in1', In(T),
                              'out', Out(out_type if out_type else T),
                              stateful=False,
                              simulate=simulate,
                              verilog_name=name,
                              default_kwargs={"width": N})

    @type_check_binary_operator
    def func(self, other):
        return Declare(self.N)()(self, other)
    func.__name__ = op
    setattr(type_type, op, func)
    return Declare

DefineCoreirEQ = declare_binop("coreir_eq", Bits, BitsType, "__eq__",
        operator.eq, out_type=Bit)

@type_check_definition_params
def DefineEQ(height=2, width=None):
    if width is None:
        return BitAnd
    elif height is 2:
        return DefineCoreirEQ(width)
    else:
        return DefineFoldOp(DefineEQ, "eq", height, width)


def EQ(height, **kwargs):
    def EQGenerator(*args):
        if all(isinstance(arg, BitType) for arg in args):
            width = None
        else:
            assert all(isinstance(arg, BitsType) for arg in args)
            width = len(args[0])
            assert all(len(arg) == width for arg in args)
        return DefineEQ(height, width)(**kwargs)(*args)
    return EQGenerator


def eq(*args):
    return EQ(len(args))(*args)

def DefineNE(*args):
    raise NotImplementedError()

def NE(*args):
    raise NotImplementedError()

def ne(*args):
    raise NotImplementedError()

# Should SAdd and UAdd be the same?
DefineSAdd = declare_binop("coreir_add", SInt, SIntType, "__add__", operator.add)
DefineSSub = declare_binop("coreir_sub", SInt, SIntType, "__sub__", operator.sub)
DefineSMul = declare_binop("coreir_mul", SInt, SIntType, "__mul__", operator.mul)
DefineSDiv = declare_binop("coreir_sdiv", SInt, SIntType, "__div__", operator.truediv)
declare_binop("coreir_sdiv", SInt, SIntType, "__truediv__", operator.truediv)

# In mantle, LT = SLT
DefineSLT = declare_binop("coreir_slt",  SInt, SIntType, "__lt__", operator.lt, out_type=Bit)
DefineSLE = declare_binop("coreir_sle", SInt, SIntType, "__le__", operator.le, out_type=Bit)
DefineSGT = declare_binop("coreir_sgt",  SInt, SIntType, "__gt__", operator.gt, out_type=Bit)
DefineSGE = declare_binop("coreir_sge", SInt, SIntType, "__ge__", operator.ge, out_type=Bit)


def simulate_neg(self, value_store, state_store):
    _in = BitVector(value_store.get_value(getattr(self, "in")), signed=True)
    out = (-_in).as_bool_list()
    value_store.set_value(self.out, out)


def DeclareNegate(N):
    return DeclareCircuit("coreir_neg{}".format(N), 'in', In(SInt(N)), 'out',
            Out(SInt(N)), simulate=simulate_neg, verilog_name="coreir_not",
            default_kwargs={"width": N})


def __neg__(self):
    return DeclareNegate(self.N)()(self)

SIntType.__neg__ = __neg__


DefineUAdd = declare_binop("coreir_add", UInt, UIntType, "__add__", operator.add)
DefineUSub = declare_binop("coreir_sub", UInt, UIntType, "__sub__", operator.sub)
DefineUMul = declare_binop("coreir_mul", UInt, UIntType, "__mul__", operator.mul)
DefineUDiv = declare_binop("coreir_udiv", UInt, UIntType, "__div__", operator.truediv)
declare_binop("coreir_udiv", UInt, UIntType, "__truediv__", operator.truediv)

DefineULT = declare_binop("coreir_ult",  UInt, UIntType, "__lt__", operator.lt, out_type=Bit)
DefineULE = declare_binop("coreir_ule", UInt, UIntType, "__le__", operator.le, out_type=Bit)
DefineUGT = declare_binop("coreir_ugt",  UInt, UIntType, "__gt__", operator.gt, out_type=Bit)
DefineUGE = declare_binop("coreir_uge", UInt, UIntType, "__ge__", operator.ge, out_type=Bit)


def arithmetic_shift_right(self, other):
    N = self.N
    T = SInt(N)
    if isinstance(other, IntegerTypes):
        if other < 0:
            raise ValueError("Second argument to arithmetic_shift_right must be "
                    "positive, not {}".format(other))

        def simulate_arithmetic_shift_right(self, value_store, state_store):
            _in = BitVector(value_store.get_value(getattr(self, "in")), signed=True)
            out = _in.arithmetic_shift_right(other)
            value_store.set_value(self.out, out.as_bool_list())
        circ =  DeclareCircuit("coreir_ashr{}".format(N), 'in', In(UInt(N)),
                'out', Out(T), verilog_name="coreir_ashr",
                simulate=simulate_arithmetic_shift_right)
        return circ(width=self.N, SHIFTBITS=other)(self)
    elif isinstance(other, Type):
        if not isinstance(other, UIntType):
            raise TypeError("Second argument to arithmetic_shift_right must be "
                    "a UInt, not {}".format(type(other)))

        def simulate(self, value_store, state_store):
            in0 = BitVector(value_store.get_value(self.in0), signed=True)
            in1 = BitVector(value_store.get_value(self.in1))
            out = in0.arithmetic_shift_right(in1).as_bool_list()
            value_store.set_value(self.out, out)

        circ = DeclareCircuit("coreir_dashr{}".format(N), 'in0', In(T), 'in1',
                In(UInt(N)), 'out', Out(T), verilog_name="coreir_dashr",
                simulate=simulate)
        return circ(width=self.N)(self, other)
    else:
        raise TypeError(">> not implemented for argument 2 of type {}".format(
            type(other)))


SIntType.arithmetic_shift_right = arithmetic_shift_right


def gen_sim_register(N, has_ce, has_reset):
    def sim_register(self, value_store, state_store):
        """
        Adapted from Brennan's SB_DFF simulation in mantle
        """
        cur_clock = value_store.get_value(self.clk)

        if not state_store:
            state_store['prev_clock'] = cur_clock
            state_store['cur_val'] = BitVector(0, num_bits=N)

        if has_reset:
            cur_reset = value_store.get_value(self.rst)
        # if s:
        #     cur_s = value_store.get_value(self.S)

        prev_clock = state_store['prev_clock']
        # if not n:
        #     clock_edge = cur_clock and not prev_clock
        # else:
        #     clock_edge = not cur_clock and prev_clock
        clock_edge = cur_clock and not prev_clock

        new_val = state_store['cur_val'].as_bool_list()

        if clock_edge:
            input_val = value_store.get_value(getattr(self, "in"))

            enable = True
            if has_ce:
                enable = value_store.get_value(self.en)

            if enable:
                # if r and sy and cur_r:
                #     new_val = False
                # elif s and sy and cur_s:
                #     new_val = True
                # else:
                #     new_val = input_val
                new_val = input_val

        if has_reset and not cur_reset:  # Reset is asserted low
            new_val = [False for _ in range(N)]
        # if s and not sy and cur_s:
        #     new_val = True

        state_store['prev_clock'] = cur_clock
        state_store['cur_val'] = BitVector(new_val, num_bits=N)
        value_store.set_value(self.out, new_val)
    return sim_register


@cache_definition
def DefineRegister(N, has_ce=False, has_reset=False, T=Bits):
    name = "coreir_reg_P"  # TODO: Add support for clock interface
    io = ["in", In(T(N)), "clk", In(Clock), "out", Out(T(N))]
    methods = []

    def reset(self, condition):
        wire(condition, self.rst)
        return self

    if has_reset:
        io.extend(["rst", In(Bit)])
        name += "R"  # TODO: This assumes ordering of clock parameters
        methods.append(circuit_type_method("reset", reset))

    def when(self, condition):
        wire(condition, self.en)
        return self

    if has_ce:
        io.extend(["en", In(Bit)])
        name += "E"  # TODO: This assumes ordering of clock parameters
        methods.append(circuit_type_method("when", when))

    return DeclareCircuit(
        name,
        *io,
        stateful=True,
        simulate=gen_sim_register(N, has_ce, has_reset),
        circuit_type_methods=methods,
        default_kwargs={"width": N}
    )


@cache_definition
def DefineMux(height=2, width=1):
    assert height == 2
    N = width
    def simulate(self, value_store, state_store):
        in0 = BitVector(value_store.get_value(self.in0))
        in1 = BitVector(value_store.get_value(self.in1))
        sel = BitVector(value_store.get_value(self.sel))
        out = in1 if sel.as_int() else in0
        value_store.set_value(self.out, out)
    return DeclareCircuit("coreir_mux".format(N), 
        *["in0", In(Bits(N)), "in1", In(Bits(N)), "sel", In(Bit), 
         "out", Out(Bits(N))],
        verilog_name="coreir_mux",
        simulate=simulate,
        default_kwargs={"width": N}
    )

def add(self, rhs):
    return self + rhs

def sub(self, rhs):
    return self - rhs

def mul(self, rhs):
    return self * rhs

def div(self, rhs):
    return self / rhs

def truediv(self, rhs):
    return self // rhs

def eq(self, rhs):
    return self == rhs

def ne(self, rhs):
    return self != rhs

def lt(self, rhs):
    return self < rhs

def le(self, rhs):
    return self <= rhs

def gt(self, rhs):
    return self > rhs

def ge(self, rhs):
    return self >= rhs

def lshift(self, rhs):
    return self << rhs

def rshift(self, rhs):
    return self >> rhs

def repeat(value, n):
    if isinstance(value, BitType):
        repeats = bits(n*[value])
    else:
        repeats = array(n*[value])
    return repeats

def concat(*arrays):
    ts = [t for a in arrays for t in a.ts] # flatten
    return array(ts)

def zext(value, n):
    assert isinstance(value, (UIntType, SIntType, BitsType))
    if isinstance(value, UIntType):
        zeros = uint(0,n)
    elif isinstance(value, SIntType):
        zeros = sint(0,n)
    elif isinstance(value, BitsType):
        zeros = bits(0,n)
    return concat(zeros,value)

def sext(value, n):
    assert isinstance(value, SIntType)
    return sint(concat(array(value[-1], n), array(value)))


#def mux(I0, I1, S):
#    assert isinstance(S, BitType)
#    assert isinstance(I0, BitType) or isinstance(I0, BitsType)
#    assert isinstance(I1, BitType) or isinstance(I1, BitsType)
#    assert type(I0) == type(I1)
#    if isinstance(I0, BitType):
#        return Mux(2)(I0, I1, S)
#    elif:
#        return Mux(2,len(I0))(I0, I1, S)

def gen_sim_mem(height, width):
    def sim_mem(self, value_store, state_store):
        cur_rclk = value_store.get_value(self.rclk)
        cur_wclk = value_store.get_value(self.wclk)

        if not state_store:
            state_store['mem'] = [
                BitVector(0, width) for _ in range(height)
            ]
            state_store['prev_rclk'] = cur_rclk
            state_store['prev_wclk'] = cur_wclk


        prev_rclk = state_store['prev_rclk']
        prev_wclk = state_store['prev_wclk']
        rclk_edge = cur_rclk and not prev_rclk
        wclk_edge = cur_wclk and not prev_wclk
        rdata = value_store.get_value(self.rdata)

        if rclk_edge:
            if value_store.get_value(self.ren):
                index = BitVector(value_store.get_value(self.raddr)).as_int()
                rdata = state_store['mem'][index].as_bool_list()
        if wclk_edge:
            if value_store.get_value(self.wen):
                index = BitVector(value_store.get_value(self.waddr)).as_int()
                state_store['mem'][index] = BitVector(value_store.get_value(self.wdata))

        state_store['prev_rclk'] = cur_rclk
        state_store['prev_wclk'] = cur_wclk
        value_store.set_value(self.rdata, rdata)
    return sim_mem

# this is different than the mantle Memory primitive
@cache_definition
def DefineMemory(height, width):
    name = "coreir_mem{}x{}".format(height,width)
    is_power_of_two = lambda num: num != 0 and ((num & (num - 1)) == 0)
    assert is_power_of_two(width) and is_power_of_two(height)
    IO = ["raddr", In(Bits(max(height.bit_length() - 1, 1))),
          "rdata", Out(Bits(width)),
          "rclk", In(Bit), 
          "ren", In(Bit), 
          "waddr", In(Bits(max(height.bit_length() - 1, 1))),
          "wdata", In(Bits(width)),
          "wclk", In(Bit), 
          "wen", In(Bit) ]
    return DeclareCircuit(name, *IO, verilog_name="coreir_mem",
            simulate=gen_sim_mem(height, width),
            default_kwargs={"width": width, "depth": height})
