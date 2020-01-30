import magma as m
import magma.testing


def test_bind():
    class RTL(m.Generator):
        @staticmethod
        def generate(width, bind=True):
            orr, andr, logical_and = m.DefineFromVerilog(f"""
module orr_{width} (input [{width - 1}:0] I, output O);
    assign O = |(I);
endmodule

module andr_{width} (input [{width - 1}:0] I, output O);
    assign O = &(I);
endmodule

module logical_and (input I0, input I1, output O);
    assign O = I0 && I1;
endmodule""")

            class HandShake(m.Product):
                ready = m.In(m.Bit)
                valid = m.Out(m.Bit)

            class Monitor(m.Circuit):
                IO = ["CLK", m.In(m.Clock),
                      "in1", m.In(m.Bits[width]),
                      "in2", m.In(m.Bits[width]),
                      "out", m.In(m.Bit),
                      "handshake", m.In(HandShake),
                      "handshake_arr", m.In(m.Array[3, HandShake]),
                      "mon_temp1", m.In(m.Bit),
                      "mon_temp2", m.In(m.Bit),
                      "intermediate_tuple", m.In(m.Tuple[m.Bit, m.Bit])]

                @classmethod
                def definition(cls):
                    cls.inline_verilog("""
                        logic temp1, temp2;
                        assign temp1 = |(in1);
                        assign temp2 = &(in1);
                        assert property (@(posedge CLK) {valid} -> out === temp1 && temp2);
                    """, valid=cls.handshake.valid)

            class RTL(m.Circuit):
                IO = ["CLK", m.In(m.Clock),
                      "in1", m.In(m.Bits[width]),
                      "in2", m.In(m.Bits[width]),
                      "out", m.Out(m.Bit),
                      "handshake", HandShake,
                      "handshake_arr", m.Array[3, HandShake]]

                @classmethod
                def definition(cls):
                    temp1 = orr()(cls.in1)
                    temp2 = andr()(cls.in1)
                    cls.out @= logical_and()(temp1, temp2)
                    m.wire(cls.handshake.valid, cls.handshake.ready)
                    for i in range(3):
                        m.wire(cls.handshake_arr[i].valid,
                               cls.handshake_arr[2 - i].ready)
                    if bind:
                        cls.bind(Monitor, temp1, temp2,
                                 m.tuple_([temp1, temp2]))
            return RTL
    RTL4 = RTL.generate(4)

    m.compile("build/bind_test", RTL4)
    assert m.testing.check_files_equal(__file__,
                                       f"build/bind_test.v",
                                       f"gold/bind_test.v")
    assert m.testing.check_files_equal(__file__,
                                       f"build/Monitor.sv",
                                       f"gold/Monitor.sv")
