import magma as m
from magma.testing import check_files_equal


def test_inline_single_instances_metadata():
    mux_aoi_2_16 = m.define_from_verilog("""
module mux_aoi_2_16 (
    input logic  [15 : 0] I0,
    input logic  [15 : 0] I1,
    input logic S,
    output logic [15 : 0] O);

    logic  [1 : 0] out_sel;
    logic  [15 : 0] O_int0;

precoder_16_2 u_precoder (
    .S(S),
    .out_sel(out_sel));

mux_logic_16_2 u_mux_logic (
    .I0 (I0),
    .I1 (I1),
    .out_sel(out_sel),
    .O0(O_int0));
    assign O = (  	O_int0 	);

endmodule""")[0]

    class MuxWrapperAOIImpl_2_16(m.Circuit):
        coreir_metadata = {"inline_single_instance": False}
        io = m.IO(I=m.In(m.Array[2, m.Bits[16]]), O=m.Out(m.Array[16, m.Bit]),
                  S=m.In(m.Array[1, m.Bit]))
        io.O @= mux_aoi_2_16()(io.I[0], io.I[1], io.S[0])

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[16]]), O=m.Out(m.Array[16, m.Bit]),
                  S=m.In(m.Array[1, m.Bit]))
        io.O @= MuxWrapperAOIImpl_2_16()(io.I, io.S)

    m.compile('build/test_inline_single_instances_metadata', Top,
              passes=["inline_single_instances"])
    assert check_files_equal(__file__,
                             "build/test_inline_single_instances_metadata.v",
                             "gold/test_inline_single_instances_metadata.v")
