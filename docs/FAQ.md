# Debugging generated verilog
## Question
How can I improve the readability of the generated Verilog?
## Answer
Set the following configuration flags at the top of your top file
```python
m.config.set_debug_mode(True)
m.set_codegen_debug_info(True)
```
This will configure magma to try to automatically capture instance names from the assigned Python variable as well as tracking the filename and line number that instances and wires are created.  This information will be produced in the output verilog file.  Please let us know if there are ways we can improve this, or if there are cases when this does not work as expected.  Note that this relies on using the `inspect` module and traversing the stack every time an instance and wire are created, which can have implications on performance for designs with large numbers of instances and wires (although this issue can usually be mitigated by leveraging decomposition, reuse, and cacheing).

# Instantiating a parametrized Verilog module
## Question
How can I instantiate a Verilog module with a set of parameters?
## Answer
Suppose I have the following module:
```verilog
// ff.v
module FF(input clk, input rst, input d, output q);

parameter init = 0;

reg ff; 
always @(posedge clk or posedge rst) begin
  if (!rst)
    ff <= init;
  else
    ff <= d; 
end

assign q = ff;
endmodule
```

I can import it into magma as follows:
```python
import magma as m


FF = m.DefineFromVerilogFile(
    "ff.v", type_map={"clk": m.In(m.Clock), "rst": m.In(m.AsyncReset)}
)[0]

class Top(m.Circuit):
    IO = ["I", m.In(m.Bits[2]), "O", m.Out(m.Bits[2])] + \
        m.ClockInterface(has_async_reset=True)
    @classmethod
    def definition(io):
        # keyword arguments to instancing call are passed as verilog parameters
        ff0 = FF(init=0)
        ff1 = FF(init=1)
        io.O <= m.join([ff0, ff1])(d=io.I, rst=io.ASYNCRESET)


m.compile("top", Top, output="coreir-verilog")
```

This produces the following Verilog, notice how the arguments to the magma
instancing call has been passed to the Verilog instancing statement.
```verilog
// top.v
module FF(input clk, input rst, input d, output q);

parameter init = 0;

reg ff; 
always @(posedge clk or posedge rst) begin
  if (!rst)
    ff <= init;
  else
    ff <= d; 
end

assign q = ff;
endmodule
module Top (input ASYNCRESET, input CLK, input [1:0] I, output [1:0] O);
wire FF_inst0_q;
wire FF_inst1_q;
FF #(.init(0)) FF_inst0(.clk(CLK), .d(I[0]), .q(FF_inst0_q), .rst(ASYNCRESET));
FF #(.init(1)) FF_inst1(.clk(CLK), .d(I[1]), .q(FF_inst1_q), .rst(ASYNCRESET));
assign O = {FF_inst1_q,FF_inst0_q};
endmodule

```

# Statically Elaborated For Loop in Combinational Circuit
## Question
How can I use a for loop that is evaluated at compile (Python) time inside
a combinational circuit definition?  For example:
```python
@m.combinational.circuit
def find_first(I: Bits[n]) -> Bits[n]:
  for i in range(n):
    if I[i]:
      return m.Bits[n](2 ** i)
  return m.Bits[n](0)
```
## Answer
This feature is forthcoming, until then, it is recommended to not use combinational
for this kind of metaprogramming, and instead use base magma. Here is an example of
writing the above circuit without the combinational syntax.
```python
class FindFirst(m.Circuit):
    IO = ["I", m.In(m.Bits[n]), "O", m.Out(m.Bits[n])]
    @classmethod
    def definition(io):
        out = m.bits(0, n)
        for i in reversed(range(n)):
            out = mantle.mux([out, m.bits(2 ** i, n)], io.I[i])
        io.O <= out
```

# fork 
## Question
For example, we have `in_data` as an input to a cell. Then I have a row module
which instantiates 10 of those cells. How do I expand `in_data` to `[in_data]*10`?

## Answer
The most idiomatic way to do this would be to use magma's fork operator, here is an
example of taking a single input `in_data` and *forking* the input to 10 instances
of an `Invert` cell.
```python
class RowInvert(m.Circuit):
    IO = ["in_data", m.In(m.Bits[8]), "out_data", m.Out(m.Array[10, m.Bits[8]])]
    @classmethod
    def definition(io):
        io.out_data <= m.fork([mantle.Invert(8) for _ in range(10)])(io.in_data)
```
See the documentation on `fork`
(https://github.com/phanrahan/magma/blob/master/docs/higher_order_circuits.md#join-flat-and-fork)
for more information.

# join vs array
## Question
I tried to instantiate an array of `mantle.CounterLoad` as follows.

```python
iter_num = m.array(
    [mantle.CounterLoad(cntr_width, cin=False, cout=False, incr=1, has_ce=True,
                        has_reset=True, name=f"iter_num_{i}") 
     for i in range(num_cntrs)]
)
```

I got the following error.

```
ValueError: All fields in a Array or a Tuple must be the same typegot CounterLoad5CER(DATA: In(UInt[5]), LOAD: In(Bit), O: Out(UInt[5]), CLK: In(Clock), CE: In(Enable), RESET: In(Reset)) expected CounterLoad5CER(DATA: In(UInt[5]), LOAD: In(Bit), O: Out(UInt[5]), CLK: In(Clock), CE: In(Enable), RESET: In(Reset))
```

## Answer
`m.array` is used to convert magma types, so one can take a list of `m.Bit`s
and convert them into an `m.Array` type.  In this case, you're trying to convert
a list of instances and "join" there interfaces into an array. For this pattern,
use magma's `m.join` higher order circuit operator:
```
iter_num = m.join(
    [mantle.CounterLoad(cntr_width, cin=False, cout=False, incr=1, has_ce=True,
                        has_reset=True, name=f"iter_num_{i}") 
     for i in range(num_cntrs)]
)
```
See
https://github.com/phanrahan/magma/blob/master/docs/higher_order_circuits.md#join-flat-and-fork
for more information.

# Dynamically Declared Circuit Interface
## Question
How do I declare a dynamically constructed circuit interface?
## Answer
There are two ways to do this using the standard subclassing `m.Circuit` syntax
and the `m.DeclareCircuit` syntax:

Option 1:
```python
def make_Declaration(n, ...):
    class Declaration(m.Circuit):
        # Create IO list
        IO = []
        # Dynamically add things to the list
        for i in range(n):
            IO += [f"I{n}", m.In(m.Bits[i + 1])]
        IO += ["O", m.Out(m.Bits[n + 1])]
    return Declaration
```

Option 2:
```python
def make_Declaration(n, ...):
    # Create IO list
    IO = []
    # Dynamically add things to the list
    for i in range(n):
        IO += [f"I{n}", m.In(m.Bits[i + 1])]
    IO += ["O", m.Out(m.Bits[n + 1])]
    # Use "splat/asterix" (*) operator to turn list into arguments to declare
    # circuit
    return m.DeclareCircuit("Declaration", *IO)
```

# Reduction Tree
## Question
How can I implement the following example verilog code for a reduction tree?
```verilog
always_comb
begin
    out = 0;
    for(int i=0;i<REDUCTION_LENGTH;i=i+1)
        out = out + in_reduction[i]
end
```

## Answer
There are two options, the above example can be directly translated using a for loop, or you can use Python's `reduce` function:
```python
def make_Reduction(n):
    class Reduction(m.Circuit):
        IO = ["in_reduction", m.In(m.Array[n, m.UInt[8]]),
              "out0", m.Out(m.UInt[8]), "out1", m.Out(m.UInt[8])]
        @classmethod
        def definition(io):
            # Option 1 with for loop
            out = m.uint(0, 8)
            for i in range(n):
                out += io.in_reduction[i]
            io.out0 <= out

            # Option 2 with reduce
            from functools import reduce
            import operator
            io.out1 <= reduce(operator.add, io.in_reduction)
	return Reduction
```

# Transpose Matrix
## Question
How can I tranpose a 2-d array?
## Answer
```python
def make_Transpose(n0, n1):
    class Transpose(m.Circuit):
        IO = ["a", m.In(m.Array[n0, m.Array[n1, m.Bit]]),
              "b", m.Out(m.Array[n1, m.Array[n0, m.Bit]])]
        @classmethod
        def definition(io):
            for col in range(n0):
                for row in range(n1):
                    m.wire(io.b[row][col], io.a[col][row])

    return Transpose
```
