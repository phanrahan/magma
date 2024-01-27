# split_verilog option

## Bind example

### Python code
---

`main.py` (note options `m.compile()`, and that the output file is in the `output/` directory):
```python
import magma as m


class Foo(m.Circuit):
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
    io.O @= io.I


class FooMonitor(m.Circuit):
    io = m.IO(**m.make_bind_ports(Foo))
    m.inline_verilog("assert I;")


m.bind(Foo, FooMonitor)


class Bar(m.Circuit):
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
    io.O @= io.I


class BarMonitor(m.Circuit):
    io = m.IO(**m.make_bind_ports(Bar))
    m.inline_verilog("assert I;")


m.bind(Bar, BarMonitor)


class Top(m.Circuit):
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
    io.O @= Foo()(Bar()(io.I))


opts = {
    "split_verilog": True,
    "sv": True,
}
m.compile("output/main", Top, output="mlir-verilog", **opts)
```

---

### Generated collateral

---
`output/main.sv` (main RTL; note how it only includes `Bar`, `Foo`, and `Top`):
```Verilog
module Bar(
  input  [7:0] I,
  output [7:0] O);

  /* This instance is elsewhere emitted as a bind statement.
    BarMonitor BarMonitor_inst0 (
      .I (I),
      .O (I)
    );
  */
  assign O = I;
endmodule

module Foo(
  input  [7:0] I,
  output [7:0] O);

  /* This instance is elsewhere emitted as a bind statement.
    FooMonitor FooMonitor_inst0 (
      .I (I),
      .O (I)
    );
  */
  assign O = I;
endmodule

module Top(
  input  [7:0] I,
  output [7:0] O);

  wire [7:0] _Bar_inst0_O;
  Bar Bar_inst0 (
    .I (I),
    .O (_Bar_inst0_O)
  );
  Foo Foo_inst0 (
    .I (_Bar_inst0_O),
    .O (O)
  );
endmodule


```
---
`ouput/BarMonitor.sv`:
```Verilog
module BarMonitor(
  input [7:0] I,
              O);

  assert I;
endmodule

bind Bar BarMonitor BarMonitor_inst0 (
  .I (I),
  .O (I)
);
```
---
`output/FooMonitor.sv`:
```Verilog
module FooMonitor(
  input [7:0] I,
              O);

  assert I;
endmodule

bind Foo FooMonitor FooMonitor_inst0 (
  .I (I),
  .O (I)
);
```
---
`output/main_bind_files.list`:
```
output/BarMonitor.sv
output/FooMonitor.sv
```
---
