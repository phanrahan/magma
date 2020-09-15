import magma as m


class RTL(m.Generator):
    @staticmethod
    def generate(width):
        orr, andr, logical_and = m.define_from_verilog(f"""
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

        class SomeCircuit(m.Circuit):
            io = m.IO(I=m.In(m.Bits[width]))
            io.I.unused()

        class RTL(m.Circuit):
            io = m.IO(CLK=m.In(m.Clock),
                      in1=m.In(m.Bits[width]),
                      in2=m.In(m.Bits[width]),
                      out=m.Out(m.Bit),
                      handshake=HandShake,
                      handshake_arr=m.Array[3, HandShake],
                      ndarr=m.In(m.Array[(2, 3), m.Bit]))

            temp1 = orr()(io.in1)
            temp2 = andr()(io.in1)
            intermediate_tuple = m.tuple_([temp1, temp2])
            intermediate_ndarr = m.Array[(3, 2), m.Bit](
                name="intermediate_ndarr"
            )
            for i in range(3):
                for j in range(2):
                    intermediate_ndarr[i, j] @= io.ndarr[j, i]
            temp3 = m.Bit(name="temp3")
            temp3 @= temp2
            temp3.unused()
            io.out @= logical_and()(intermediate_tuple[0],
                                    intermediate_tuple[1])
            m.wire(io.handshake.valid, io.handshake.ready)
            for i in range(3):
                m.wire(io.handshake_arr[i].valid,
                       io.handshake_arr[2 - i].ready)

            some_circ = SomeCircuit()
            some_circ.I @= io.in1 ^ io.in2
            m.as_bits(io.ndarr).unused()
        return RTL
