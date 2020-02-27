import magma as m


class RTL(m.Generator):
    @staticmethod
    def generate(width):
        orr, andr, logical_and = m.DefineFromVerilog(f"""
            module orr_{width} (input [{width - 1}:0] I, output O);
            assign O = |(I);
            endmodule

            module andr_{width} (input [{width - 1}:0] I, output O);
            assign O = &(I);
            endmodule

            module logical_and (input I0, input I1, output O);
            assign O = I0 && I1;
            endmodule
        """)

        class HandShake(m.Product):
            ready = m.In(m.Bit)
            valid = m.Out(m.Bit)

        class RTL(m.Circuit):
            IO = ["CLK", m.In(m.Clock),
                  "in1", m.In(m.Bits[width]),
                  "in2", m.In(m.Bits[width]),
                  "out", m.Out(m.Bit),
                  "handshake", HandShake,
                  "handshake_arr", m.Array[3, HandShake]]

            @classmethod
            def definition(cls):
                cls.temp1 = orr()(cls.in1)
                cls.temp2 = andr()(cls.in1)
                cls.intermediate_tuple = m.tuple_([cls.temp1, cls.temp2])
                cls.out @= logical_and()(cls.intermediate_tuple[0],
                                         cls.intermediate_tuple[1])
                m.wire(cls.handshake.valid, cls.handshake.ready)
                for i in range(3):
                    m.wire(cls.handshake_arr[i].valid,
                           cls.handshake_arr[2 - i].ready)
        return RTL
