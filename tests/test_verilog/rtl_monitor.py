import magma as m
from rtl import RTL


class RTLMonitor(m.MonitorGenerator):
    @staticmethod
    def generate_bind(circuit, width):
        # circuit is a reference to the generated module (to retrieve
        # internal signals)
        class RTLMonitor(m.Circuit):
            IO = m.MonitorIO(circuit)
            IO += ["mon_temp1", m.In(m.Bit),
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

        circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2)


RTL.bind(RTLMonitor)
