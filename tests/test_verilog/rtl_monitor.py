import magma as m
from rtl import RTL


class RTLMonitor(m.MonitorGenerator):
    @staticmethod
    def generate_bind(circuit, width):
        # circuit is a reference to the generated module (to retrieve internal
        # signals and bind to the module)
        class RTLMonitor(m.Circuit):
            IO = m.MonitorIO(circuit)
            IO += ["mon_temp1", m.In(m.Bit),
                   "mon_temp2", m.In(m.Bit),
                   "intermediate_tuple", m.In(m.Tuple[m.Bit, m.Bit])]

            @classmethod
            def definition(cls):
                cls.inline_verilog("""
logic temp1, temp2;
logic [{width}:0] temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & {x};
assign temp3 = in0 ^ in1;
assert property (@(posedge CLK) {valid} -> out === temp1 && temp2);
                                   """,
                                   valid=cls.handshake.valid,
                                   width=width - 1,
                                   x=cls.intermediate_tuple[0])

        circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2)


RTL.bind(RTLMonitor)
