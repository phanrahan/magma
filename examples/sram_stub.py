import magma as m
# Import mantle to define operators
import mantle


# Returns a list of modules, select the only one
SRAM_512W_16B = m.define_from_verilog_file("examples/sram_stub.v",
                                           target_modules=["sram_512w_16b"],
                                           # Convert CLK port from raw Bit to
                                           # magma clock type
                                           type_map={"CLK": m.In(m.Clock)})[0]


# ported from
# https://github.com/StanfordAHA/CGRAGenerator/blob/master/hardware/generator_z/memory_core/mem.vp
class Mem(m.Circuit):
    io = m.IO(data_out=m.Out(m.Bits[16]),
              data_in=m.In(m.Bits[16]),
              clk=m.In(m.Clock),
              cen=m.In(m.Enable),
              wen=m.In(m.Enable),
              addr=m.In(m.Bits[9]))

    # Instance sram
    sram = SRAM_512W_16B(name="mem_inst")
    # Wire up io
    io.data_out @= sram.Q
    sram.CLK @= io.clk
    sram.A @= io.addr
    sram.D @= io.data_in
    # Invert control signals
    # We convert from enable type to bit type to define invert operator
    # (enables do not have operators by default)
    sram.CEN @= ~m.bit(io.cen)
    sram.WEN @= ~m.bit(io.wen)
    # Set constants
    sram.EMA @= 0
    sram.EMAW @= 0
    sram.EMAS @= 0
    sram.TEN @= 1
    sram.BEN @= 1
    sram.RET1N @= 1
    sram.STOV @= 0


m.compile("examples/build/mem", Mem, inline=True)
