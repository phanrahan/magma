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
                      intermediate_tuple=m.In(m.Tuple[m.Bit, m.Bit]))

            # NOTE: Needs to have a name
            arr_2d = m.Array[2, m.Bits[width]](name="arr_2d")
            for i in range(2):
                arr_2d[i] @= getattr(io, f"in{i + 1}")
            m.inline_verilog("""
logic temp1, temp2;
logic [{width}-1:0] temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & {x};
assign temp3 = in1 ^ in2;
assert property (@(posedge CLK) {valid} -> out === temp1 && temp2);
logic [{width}-1:0] temp4 [1:0];
assign temp4 = {arr_2d};
                                   """,
                                   valid=io.handshake.valid,
                                   width=width,
                                   x=io.intermediate_tuple[0],
                                   arr_2d=arr_2d)

        circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2,
                     circuit.intermediate_tuple)


RTL.bind(RTLMonitor)
