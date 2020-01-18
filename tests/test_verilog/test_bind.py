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

            class Monitor(m.Circuit):
                IO = ["CLK", m.In(m.Clock),
                      "in1", m.In(m.Bits[width]),
                      "in2", m.In(m.Bits[width]),
                      "out", m.In(m.Bit),
                      "mon_temp1", m.In(m.Bit),
                      "mon_temp2", m.In(m.Bit)]

                @classmethod
                def definition(cls):
                    cls.verilog = """
                        logic temp1, temp2;
                        assign temp1 = |(in1);
                        assign temp2 = &(in1);
                        assert property (@(posedge CLK) out === temp1 && temp2);
                    """

            class RTL(m.Circuit):
                IO = ["CLK", m.In(m.Clock),
                      "in1", m.In(m.Bits[width]),
                      "in2", m.In(m.Bits[width]),
                      "out", m.Out(m.Bit)]

                @classmethod
                def definition(cls):
                    temp1 = orr()(cls.in1)
                    temp2 = andr()(cls.in1)
                    cls.out @= logical_and()(temp1, temp2)
                    if bind:
                        cls.bind(Monitor, temp1, temp2)
            return RTL
    RTL4 = RTL.generate(4)

    m.compile("build/bind_test", RTL4)
    assert m.testing.check_files_equal(__file__,
                                       f"build/bind_test.v",
                                       f"gold/bind_test.v")
    assert m.testing.check_files_equal(__file__,
                                       f"build/Monitor.sv",
                                       f"gold/Monitor.sv")
