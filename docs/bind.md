# Bind

To use the `bind` feature, define a subclass of `m.MonitorGenerator` which is
bound to a subclass of `m.Generator` (design generator).  The subclass defines
a staticmethod `generate_bind(circuit, *args, **kwargs)` where `args` and
`kwargs` are the same as the corresponding `m.Generator`'s `generate` method
(reference to the same parameters).  This staticmethod should generate a
monitor circuit and call `circuit.bind(monitor, *args)`.  Extra arguments to
the `bind` method can be used to pass circuit intermediate values.

Here is a full example:

We begin with an `m.Generator` definition for some RTL.
```python
# rtl.py
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

        class RTL(m.Circuit):
            io = m.IO(CLK=m.In(m.Clock),
                      in1=m.In(m.Bits[width]),
                      in2=m.In(m.Bits[width]),
                      out=m.Out(m.Bit),
                      handshake=HandShake,
                      handshake_arr=m.Array[3, HandShake])

            temp1 = orr()(io.in1)
            temp2 = andr()(io.in1)
            intermediate_tuple = m.tuple_([temp1, temp2])
            io.out @= logical_and()(intermediate_tuple[0],
                                    intermediate_tuple[1])
            m.wire(io.handshake.valid, io.handshake.ready)
            for i in range(3):
                m.wire(io.handshake_arr[i].valid,
                       io.handshake_arr[2 - i].ready)
        return RTL
```

We define a corresponding `m.MonitorGenerator`

```python
# rtl_monitor.py
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
logic [{width-1}:0] temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & {io.intermediate_tuple[0]};
assign temp3 = in1 ^ in2;
assert property (@(posedge CLK) {valid} -> out === temp1 && temp2);
logic [{width-1}:0] temp4 [1:0];
assign temp4 = {arr_2d};
                                   """,
                                   valid=io.handshake.valid)

        circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2,
                     circuit.intermediate_tuple)


RTL.bind(RTLMonitor)
```

To bring it all together in another file, we can import `rtl` and `rtl_monitor`
```python
from rtl import RTL
import rtl_monitor
import magma as m

RTL4 = RTL.generate(4)

m.compile("build/bind_test", RTL4, inline=True)
```

If you don't want to enable the bind, simply do not import `rtl_monitor`

The `bind` statement also supports an optional `compile_guard=` keyword
argument that allows the user to wrap the generated bind statement inside a
verilog `ifdef`.  Here's an example:

```python
circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2,
             circuit.intermediate_tuple, compile_guard="BIND_ON")
# generates
# `ifdef BIND_ON
# bind ...
# endif
```
