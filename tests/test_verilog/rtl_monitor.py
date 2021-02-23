import magma as m
from rtl import RTL


class RTLMonitor(m.MonitorGenerator):
    @staticmethod
    def generate_bind(circuit, width):
        # circuit is a reference to the generated module (to retrieve internal
        # signals and bind to the module)
        class RTLMonitor(m.Circuit):
            io = m.IO(**m.make_monitor_ports(circuit),
                      mon_temp1=m.In(m.Bit),
                      mon_temp2=m.In(m.Bit),
                      intermediate_tuple=m.In(m.Tuple[m.Bit, m.Bit]),
                      inst_input=m.In(m.Bits[width]),
                      mon_temp3=m.In(m.Bit),
                      intermediate_ndarr=m.In(m.Array[(3, 2), m.Bit]),
                      tuple_arr=m.In(m.Array[1, m.UInt[20]]))

            # NOTE: Needs to have a name
            arr_2d = m.Array[2, m.Bits[width]](name="arr_2d")
            for i in range(2):
                arr_2d[i] @= getattr(io, f"in{i + 1}")
            m.inline_verilog("""
logic temp1, temp2;
logic temp3;
assign temp1 = |({io.in1});
assign temp2 = &({io.in1}) & {io.intermediate_tuple[0]};
assign temp3 = temp1 ^ temp2 & {arr_2d[0][1]};
assert property (@(posedge {io.CLK}) {valid} -> {io.out} === temp1 && temp2);
logic [{width-1}:0] temp4 [1:0];
assign temp4 = {arr_2d};
always @(*) $display("%x", {io.inst_input} & {{{width}{{{io.mon_temp3}}}}});
logic temp5;
assign temp5 = {io.intermediate_ndarr[1, 1]};
                                   """,
                                   valid=io.handshake.valid)

        circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2,
                     circuit.intermediate_tuple, circuit.some_circ.I,
                     circuit.temp3, circuit.intermediate_ndarr,
                     circuit.nested_other_circ.other_circ.x.y,
                     compile_guard="BIND_ON")


RTL.bind(RTLMonitor)
