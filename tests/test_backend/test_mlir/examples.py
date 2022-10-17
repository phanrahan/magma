import itertools

import magma as m
from magma.inline_verilog import ProcessInlineVerilogPass
from magma.passes.drive_undriven import drive_undriven
from magma.testing.utils import SimpleMagmaProtocol


class simple_comb(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), b=m.In(T), c=m.In(T), y=m.Out(T), z=m.Out(T))
    a = ~io.a
    o = io.a | a
    o = o | io.b
    io.y @= o
    io.z @= o


class simple_hierarchy(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), b=m.In(T), c=m.In(T), y=m.Out(T), z=m.Out(T))
    y, z = simple_comb()(io.a, io.b, io.c)
    io.y @= y
    io.z @= z


class simple_aggregates_bits(m.Circuit):
    T = m.Bits[16]
    U = m.Bits[8]
    io = m.IO(a=m.In(T), y=m.Out(T), z=m.Out(U))
    half = int(T.N / 2)
    io.y[:half] @= io.a[half:]
    io.y[half:] @= io.a[:half]
    io.z @= io.a[:half]


class simple_aggregates_array(m.Circuit):
    T = m.Array[8, m.Bits[16]]
    U = m.Array[4, m.Bits[16]]
    io = m.IO(a=m.In(T), y=m.Out(T), z=m.Out(U))
    half = int(T.N / 2)
    io.y[:half] @= io.a[half:]
    io.y[half:] @= io.a[:half]
    io.z @= io.a[:half]


class simple_aggregates_nested_array(m.Circuit):
    T = m.Array[8, m.Array[4, m.Bits[16]]]
    io = m.IO(a=m.In(T), y=m.Out(T))
    half = int(T.N / 2)
    io.y[:half] @= io.a[half:]
    io.y[half:] @= io.a[:half]


class complex_aggregates_nested_array(m.Circuit):
    T = m.Array[2, m.Array[3, m.Bits[4]]]
    io = m.IO(a=m.In(T), y=m.Out(T))

    I, J, K = T.N, T.T.N, T.T.T.N
    for i, j, k in itertools.product(range(I), range(J), range(K)):
        i1, j1, k1 = I - i - 1, J - j - 1, K - k - 1
        a0 = io.a[i][j][k]
        a1 = io.a[i1][j1][k1]
        io.y[i][j][k] @= a0 | a1


class simple_aggregates_product(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=S, y=S))
    io = m.IO(a=m.In(T), y=m.Out(T))
    io.y.x @= ~io.a.x
    io.y.y @= ~io.a.y


class simple_aggregates_tuple(m.Circuit):
    S = m.Bits[8]
    T = m.Tuple[S, S]
    io = m.IO(a=m.In(T), y=m.Out(T))
    io.y[0] @= ~io.a[0]
    io.y[1] @= ~io.a[1]


class simple_constant(m.Circuit):
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
    io.O @= io.I << 1


class aggregate_constant(m.Circuit):
    T = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bits[4]))
    io = m.IO(y=m.Out(T))
    y = T(m.Bits[8](0), m.Bits[4](0))
    io.y @= y


class simple_mux_wrapper(m.Circuit):
    T = m.Bits[8]
    io = m.IO(a=m.In(T), s=m.In(m.Bit), y=m.Out(T))
    io.y @= m.mux([io.a, ~io.a], io.s)


class aggregate_mux_wrapper(m.Circuit):
    T = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))
    io = m.IO(a=m.In(T), s=m.In(m.Bit), y=m.Out(T))
    not_a = T(*map(lambda x: ~x, io.a))
    io.y @= m.mux([io.a, not_a], io.s)


class non_power_of_two_mux_wrapper(m.Circuit):
    T = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))
    io = m.IO(a=m.In(T), s=m.In(m.Bits[4]), y=m.Out(T))
    not_a = T(*map(lambda x: ~x, io.a))
    inputs = [io.a, not_a]
    inputs += [not_a] * 10
    io.y @= m.mux(inputs, io.s)


class simple_register_wrapper(m.Circuit):
    T = m.Bits[8]
    io = m.IO(a=m.In(T), y=m.Out(T))
    io.y @= m.register(io.a, init=3, name="reg0")


class complex_register_wrapper(m.Circuit):
    T0 = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))
    T1 = m.Array[6, m.Bits[16]]
    T2 = m.Product.from_fields("anon", dict(u=T0, v=T1))
    io = m.IO(a=m.In(T0), b=m.In(T1), y=m.Out(T2))
    io += m.ClockIO(has_enable=True, has_async_reset=True)
    # reg_a has both a reset and enable signal. reg_b has only a reset signal,
    # and reg_c has only an enable signal. reg_a and reg_b have complex types,
    # and init values.
    reg_a = m.register(
        io.a, init=T0(10, 1), reset_type=m.AsyncReset, has_enable=True)
    reg_b = m.register(io.b, init=T1(*(i * 2 for i in range(T1.N))))
    reg_c = m.register(io.a.x, has_enable=True)
    y = T2(reg_a, reg_b)
    io.y @= y


class counter(m.Circuit):
    T = m.UInt[16]
    io = m.IO(y=m.Out(T)) + m.ClockIO()
    O = T()
    reg = m.Register(T)()
    O @= reg.O
    reg.I @= O + 1
    io.y @= O


m.passes.clock.WireClockPass(counter).run()


class _twizzler(m.Circuit):
    name = "twizzler"
    io = m.IO(
        I0=m.In(m.Bit), I1=m.In(m.Bit), I2=m.In(m.Bit),
        O0=m.Out(m.Bit), O1=m.Out(m.Bit), O2=m.Out(m.Bit))
    io.O0 @= ~io.I1
    io.O1 @= ~io.I0
    io.O2 @= ~io.I2


class twizzle(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    t0 = _twizzler(name="t0")
    t1 = _twizzler(name="t1")
    t0.I0 @= io.I
    t0.I1 @= t1.O0
    t0.I2 @= t1.O1
    t1.I0 @= t0.O0
    t1.I1 @= t0.O1
    t1.I2 @= t0.O2
    io.O @= t1.O2


class simple_unused_output(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), b=m.In(T), c=m.In(T), y=m.Out(T))
    _, z = simple_comb()(io.a, io.b, io.c)
    io.y @= z


class feedthrough(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I


class no_outputs(m.Circuit):
    io = m.IO(I=m.In(m.Bit))
    ~io.I


class simple_mixed_direction_ports(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=m.In(S), y=m.Out(S)))
    io = m.IO(a=T)
    io.a.y @= io.a.x


class complex_mixed_direction_ports(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=m.In(S), y=m.Out(S)))
    io = m.IO(a=m.Array[8, T], b=T.flip())
    m.wire(io.a[1], io.b)
    for i, aa in enumerate(io.a):
        if i == 1: continue
        aa.y @= 0


class complex_mixed_direction_ports2(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=m.In(S), y=m.Out(S)))
    io = m.IO(a=T)
    simple = simple_mixed_direction_ports()
    m.wire(io.a.x, simple.a.x)
    m.wire(io.a.y, simple.a.y)


class simple_decl(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))


class simple_decl_external(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= simple_decl()(io.I)


class simple_verilog_defn(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    verilog = "assign O = I;"


class simple_verilog_defn_wrapper(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= simple_verilog_defn()(io.I)


class simple_length_one_array(m.Circuit):
    io = m.IO(I=m.In(m.Array[1, m.Bits[8]]), O=m.Out(m.Bits[8]))
    io.O @= io.I[0]


class simple_length_one_bits(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bits[1]))
    io.O[0] @= io.I


class simple_array_of_bit(m.Circuit):
    T = m.Array[8, m.Bit]
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= T(list(reversed(io.I)))


class simple_reduction(m.Circuit):
    T = m.Bits[8]
    io = m.IO(
        I0=m.In(T), I1=m.In(T), I2=m.In(T),
        O0=m.Out(m.Bit), O1=m.Out(m.Bit), O2=m.Out(m.Bit)
    )
    io.O1 @= io.I1.reduce_or()
    io.O0 @= io.I0.reduce_and()
    io.O2 @= io.I2.reduce_xor()


class simple_shifts(m.Circuit):
    T0 = m.Bits[8]
    T1 = m.SInt[8]
    io = m.IO(
        I00=m.In(T0), I01=m.In(T0), O0=m.Out(T0),
        I10=m.In(T0), I11=m.In(T0), O1=m.Out(T0),
        I20=m.In(T1), I21=m.In(T1), O2=m.Out(T1)
    )
    io.O0 @= io.I00 << io.I01
    io.O1 @= io.I10 >> io.I11
    io.O2 @= io.I20 >> io.I21


class simple_wire(m.Circuit):
    T = m.Bits[8]
    io = m.IO(I=m.In(T), O=m.Out(T))
    tmp = T(name="tmp")
    tmp @= io.I
    io.O @= tmp


class complex_wire(m.Circuit):
    Ts = (m.Bits[8], m.Reset, m.Array[4, m.Bits[8]],)
    io = m.IO(
        **{f"I{i}": m.In(T) for i, T in enumerate(Ts)},
        **{f"O{i}": m.Out(T) for i, T in enumerate(Ts)}
    )
    for i in range(3):
        I = getattr(io, f"I{i}")
        O = getattr(io, f"O{i}")
        tmp = Ts[i](name=f"tmp{i}")
        tmp @= I
        O @= tmp


m.backend.coreir.insert_coreir_wires.insert_coreir_wires(simple_wire)
m.backend.coreir.insert_coreir_wires.insert_coreir_wires(complex_wire)


class simple_wrap_cast(m.Circuit):
    io = m.IO(I=m.In(m.Clock), O=m.Out(m.Bit))
    io.O @= m.Bit(io.I)


m.backend.coreir.insert_wrap_casts.insert_wrap_casts(simple_wrap_cast)


class simple_redefinition_module0(m.Circuit):
    name = "simple_redefinition_module"
    io = m.IO(a=m.In(m.Bit), y=m.Out(m.Bit))
    io.y @= io.a


class simple_redefinition_module1(m.Circuit):
    name = "simple_redefinition_module"
    io = m.IO(a=m.In(m.Bit), y=m.Out(m.Bit))
    io.y @= io.a


class simple_redefinition(m.Circuit):
    io = m.IO(a=m.In(m.Bit), y=m.Out(m.Bit))
    i0 = simple_redefinition_module0()
    i1 = simple_redefinition_module1()
    io.y @= i1(i0(io.a))


class simple_lut(m.Circuit):
    T = m.Bits[8]
    io = m.IO(a=m.In(m.Bits[2]), y=m.Out(T))
    values = T(0xDE), T(0xAD), T(0xBE), T(0xEF)
    io.y @= m.LUT(T, values)()(io.a)


class complex_lut(m.Circuit):
    T0 = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))
    T = m.Array[2, T0]
    T_flat = m.Bits[T.flat_length()]
    io = m.IO(a=m.In(m.Bits[2]), y=m.Out(T))
    values = T_flat(71183), T_flat(100207), T_flat(234315), T_flat(140574)
    io.y @= m.LUT(T, values)()(io.a)


class simple_side_effect_instance(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    no_outputs()(io.I)
    io.O @= io.I


class simple_inline_verilog(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I
    m.inline_verilog(
"""
	// This is 'a' "comment".
""")


class complex_inline_verilog(m.Circuit):
    io = m.IO(I=m.In(m.Bits[12]), O=m.Out(m.Bits[12]))
    io.O @= m.register(io.I)
    string = "\n".join(
        f"assert property (@(posedge CLK) {{I{i}}} |-> ##1 {{O{i}}});"
        for i in range(12)
    )
    refs = {}
    for i in range(12):
        refs[f"I{i}"] = io.I[i]
        refs[f"O{i}"] = io.O[i]
    m.inline_verilog(string, **refs)
    m.inline_verilog("// A fun{{k}}y comment with {I}", I=io.I)


class simple_bind(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= m.register(io.I)


class simple_bind_asserts(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.In(m.Bit)) + m.ClockIO()
    m.inline_verilog(
        "assert property (@(posedge CLK) {I} |-> ##1 {O});",
        O=io.O, I=io.I
    )


ProcessInlineVerilogPass(simple_bind_asserts).run()
simple_bind.bind(simple_bind_asserts)
m.passes.clock.WireClockPass(simple_bind).run()
m.passes.clock.WireClockPass(simple_bind_asserts).run()


class complex_bind(m.Circuit):
    T = m.Product.from_fields("anon", dict(I=m.Bit))
    io = m.IO(I=m.In(T), O=m.Out(m.Bit))
    not_I = ~io.I.I
    io.O @= m.register(~not_I)


class complex_bind_asserts(m.Circuit):
    T = complex_bind.T
    io = m.IO(I=m.In(T), O=m.In(m.Bit)) + m.ClockIO() + m.IO(I0=m.In(m.Bit))
    m.inline_verilog(
        "assert property (@(posedge CLK) {I} |-> ##1 {O});"
        "assert property ({I} |-> {I0};",
        O=io.O, I=io.I.I, I0=io.I0
    )


ProcessInlineVerilogPass(complex_bind_asserts).run()
complex_bind.bind(complex_bind_asserts, complex_bind.not_I)
m.passes.clock.WireClockPass(complex_bind).run()
m.passes.clock.WireClockPass(complex_bind_asserts).run()


class xmr_bind_grandchild(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), y=m.Out(T))
    io.y @= io.a


class xmr_bind_child(m.Circuit):
    T = xmr_bind_grandchild.T
    io = m.IO(a=m.In(T), y=m.Out(T))
    inst = xmr_bind_grandchild()
    inst.a @= io.a
    io.y @= inst.y


class xmr_bind(m.Circuit):
    T = xmr_bind_grandchild.T
    io = m.IO(a=m.In(T), y=m.Out(T))
    inst = xmr_bind_child()
    inst.a @= io.a
    io.y @= inst.y


class xmr_bind_asserts(m.Circuit):
    T = xmr_bind.T
    io = m.IO(a=m.In(T), y=m.In(T), other=m.In(T))
    m.inline_verilog("assert property ({other} == 0);", other=io.other)


ProcessInlineVerilogPass(xmr_bind_asserts).run()
xmr_bind.bind(xmr_bind_asserts, xmr_bind.inst.xmr_bind_grandchild_inst0.y)


class simple_compile_guard(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()
    with m.compile_guard(
            "COND1", defn_name="COND1_compile_guard", type="defined"):
        out = m.Register(m.Bit)()(io.I)
    with m.compile_guard(
            "COND2", defn_name="COND2_compile_guard", type="undefined"):
        out = m.Register(m.Bit)()(io.I)
    io.O @= io.I


m.passes.clock.WireClockPass(simple_compile_guard).run()


class simple_custom_verilog_name(m.Circuit):
    coreir_metadata = {"verilog_name": "simple_custom_verilog_name_custom_name"}
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I


class simple_module_params(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I

    coreir_config_param_types = {"width": int, "height": int}


class simple_module_params_instance(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    inst = simple_module_params(width=10, height=20)
    io.O @= inst(io.I)


class simple_undriven(m.Circuit):
    io = m.IO(O=m.Out(m.Bit))
    io.O.undriven()


class complex_undriven(m.Circuit):
    T = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))
    io = m.IO(O=m.Out(T))
    io.O.undriven()


class simple_memory_wrapper(m.Circuit):
    T = m.Bits[12]
    height = 128
    addr_type = m.Bits[m.bitutils.clog2(128)]
    io = m.IO(
        RADDR=m.In(addr_type),
        RDATA=m.Out(T),
        CLK=m.In(m.Clock),
        WADDR=m.In(addr_type),
        WDATA=m.In(T),
        WE=m.In(m.Enable),
    )
    mem = m.Memory(height=height, T=T)()
    io.RDATA @= mem(
        RADDR=io.RADDR,
        RDATA=io.RDATA,
        WADDR=io.WADDR,
        WDATA=io.WDATA,
        WE=io.WE,
    )


m.passes.clock.WireClockPass(simple_memory_wrapper).run()


class simple_undriven_instances(m.Circuit):
    io = m.IO()
    simple_comb()
    simple_comb()


drive_undriven(simple_undriven_instances)


class simple_neg(m.Circuit):
    T = m.UInt[8]
    io = m.IO(a=m.In(T), y=m.Out(T))
    io.y @= -io.a


class simple_array_slice(m.Circuit):
    T = m.Bits[8]
    io = m.IO(a=m.In(m.Array[12, T]), y=m.Out(m.Array[4, T]))
    io.y @= io.a[:4]


class complex_when_lazy_tuple(m.Circuit):
    T = m.Tuple[m.Bit, m.Bits[8]]
    io = m.IO(I0=m.In(T), I1=m.In(T), S=m.In(m.Bit), O=m.Out(T))
    x = T(name="x")
    with m.when(io.S):
        x @= io.I0
    with m.otherwise():
        x @= io.I1

    io.O @= x


class simple_magma_protocol(m.Circuit):
    T = SimpleMagmaProtocol[m.Bits[8]]
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= io.I


class simple_smart_bits(m.Circuit):
    T = m.smart.SmartBits[8]
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= io.I


class complex_magma_protocol(m.Circuit):
    T = simple_magma_protocol.T
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= simple_magma_protocol()(io.I)
