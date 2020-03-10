# Inserting Header and Footer in Generated Verilog
This is only supported using the default `coreir-verilog` output target.

Suppose you have a header in a file such as `header.v` containing a comment string
that you'd like to include in the generated verilog (e.g. a copyright notice):

```verilog
/*
This is a test header, useful for something like a copyright that you'd like to
include in all your generated files
*/
```

You can include this header with the keyword argument
`header_file="<file_name>"` for `m.compile`.

You can also insert a simple string using the `header_str="<string>"` argument,
useful for inserting something like an `` `ifdef``.  Similarly , there is a
`footer_str="<string>"` argument that will be appended to the end of the file,
useful for somehting like an `` `endif``.  If `header_str` and `header_file` are
both specified, the file will be inserted before the string.

Here's a full example:
```python
class Foo(m.Circuit):
    io = m.IO(x=m.In(m.Bit), y=m.Out(m.Bit))

class Main(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    foo = Foo()
    foo.x @= io.I
    io.O @= foo.y

m.compile("build/test_header_footer", Main, header_file="header.v",
          header_str="`ifdef FOO", footer_str="`endif")
```

This produces the following output
```verilog
/*
This is a test header, useful for something like a copyright that you'd like to
include in all your generated files
*/

`ifdef FOO
// Module `Foo` defined externally
module Main (
    input I,
    output O
);
wire Foo_inst0_y;
Foo Foo_inst0 (
    .x(I),
    .y(Foo_inst0_y)
);
assign O = Foo_inst0_y;
endmodule


`endif
```
