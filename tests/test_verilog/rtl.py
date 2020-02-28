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
            io = m.IO(CLK=m.In(m.Clock),
                      in1=m.In(m.Bits[width]),
                      in2=m.In(m.Bits[width]),
                      out=m.Out(m.Bit),
                      handshake=HandShake,
                      handshake_arr=m.Array[3, HandShake])

            temp1 = orr()(io.in1)
            temp2 = andr()(io.in1)
            io.out @= logical_and()(temp1, temp2)
            m.wire(io.handshake.valid, io.handshake.ready)
            for i in range(3):
                m.wire(io.handshake_arr[i].valid,
                       io.handshake_arr[2 - i].ready)
        return RTL
