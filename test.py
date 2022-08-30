import magma as m


class Foo(m.Circuit):
    io = m.IO(I=m.In(m.Bits[32]), O=m.Out(m.Bit))
    x = m.Bits[8]()
    x @= io.I[:8]
    m.inline_verilog("`ifdef TRG_LOGGING_ON")
    m.inline_verilog("$display(\"%x\", {io.I[0]});")
    m.inline_verilog("`endif TRG_LOGGING_ON")
    io.O @= io.I[0]


m.compile("build/Foo", Foo, output="mlir-verilog")
