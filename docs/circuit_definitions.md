**NOTE The combinational and sequential syntaxes are being deprecated, please
use combinational2 and sequential2, documneted [here](./syntaxes.md)**
**NOTE** The combinational and sequential syntax exetensions have only been
tested with the "coreir" and "coreir-verilog" compile targets.  Please set
`output="coreir-verilog"` or `output="coreir"` when calling `m.compile` to use
this feature.

# Combinational Circuit Definitions
Circuit defintions can be marked with the `@m.circuit.combinational` decorator.
This introduces a set of syntax level features for defining combinational magma
circuits, including the use of `if` statements to generate `Mux`es.

This feature is currently experimental, and therefor expect bugs to occur.
Please file any issues on the magma GitHub repository.


## If and Ternary
The condition must be an expression that evaluates to a `magma` value.

Basic example:
```python
@m.circuit.combinational
def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]

```

For reference, here is the code produced for the corresponding magma circuit
definition where the if statement has been lowered into a multiplexer:
```python
basic_if = DefineCircuit("basic_if", "I", In(Bits[2]), "S", In(Bit), "O", Out(Bit))
Mux2xOutBit_inst0 = Mux2xOutBit()
wire(basic_if.I[1], Mux2xOutBit_inst0.I0)
wire(basic_if.I[0], Mux2xOutBit_inst0.I1)
wire(basic_if.S, Mux2xOutBit_inst0.S)
wire(Mux2xOutBit_inst0.O, basic_if.O)
EndCircuit()
```

Basic nesting:
```python
@m.circuit.combinational
def if_statement_nested(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
    if S[0]:
        if S[1]:
            return I[0]
        else:
            return I[1]
    else:
        if S[1]:
            return I[2]
        else:
            return I[3]
```

Terneray expressions
```python
def ternary(I: m.Bits[2], S: m.Bit) -> m.Bit:
    return I[0] if S else I[1]
```

Nesting terneray expressions
```python
@m.circuit.combinational
def ternary_nested(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
    return I[0] if S[0] else I[1] if S[1] else I[2]
```

## Function composition:
```python
@m.circuit.combinational
def basic_if_function_call(I: m.Bits[2], S: m.Bit) -> m.Bit:
    return basic_if(I, S)
```
Function calls must refer to another `m.circuit.combinational` element, or a
function that accepts magma values, define instances and wires values, and
returns a magma.  Calling any other type of function has undefined behavior.

## Returning multiple values (tuples)

There are two ways to return multiple values, first is to use a Python tuple.
This is specified in the type signature as `(m.Type, m.Type, ...)`.  In the
body of the definition, the values can be returned using the standard Python
tuple syntax.  The circuit defined with a Python tuple as an output type will
default to the naming convetion `O0, O1, ...` for the output ports.

```python
@m.circuit.combinational
def return_py_tuple(I: m.Bits[2]) -> (m.Bit, m.Bit):
    return I[0], I[1]
```

The other method is to use an `m.Tuple` (magma's tuple type).  Again, this is
specified in the type signature, using `m.Tuple(m.Type, m.Type, ...)`.  You can
also use the namedtuple pattern to give your multiple outputs explicit names
with `m.Tuple(O0=m.Bit, O1=m.Bit)`.


```python
@m.circuit.combinational
def return_magma_tuple(I: m.Bits[2]) -> m.Tuple[m.Bit, m.Bit]:
    return m.tuple_([I[0], I[1]])
```

```python
@m.circuit.combinational
def return_magma_named_tuple(I: m.Bits[2]) -> m.Product.from_fields("anon", {"x": m.Bit, "y": m.Bit}):
    return m.namedtuple(x=I[0], y=I[1])
```

## Using non-combinational magma circuits
The combinational syntax allows the use of other combinational circuits using
the function call syntax to wire inputs and retrieve outputs.

Here is an example:
```python
class EQ(m.Circuit):
    IO = ["I0", m.In(m.Bit), "I1", m.In(m.Bit), "O", m.Out(m.Bit)]

@m.circuit.combinational
def logic(a: m.Bit) -> (m.Bit,):
    if EQ()(a, m.bit(0)):
        c = m.bit(1)
    else:
        c = m.bit(0)
    return (c,)
```

## Using magma's higher order circuits
```python
class Not(m.Circuit):
    IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

@m.circuit.combinational
def logic(a: m.Bits[10]) -> m.Bits[10]:
    return m.join(m.map_(Not, 10))(a)
```

## Using combinational circuits as a standard circuit definition
Combinational circuits can also be used as standard circuit definitions by
using the `.circuit_definition` attribute to retrieve the corresponding magma
circuit.
```python
@m.circuit.combinational
def invert(a: m.Bit) -> m.Bit:
    return Not()(a)

class Foo(m.Circuit):
    IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

    @classmethod
    def definition(io):
        # reference circuit_definition and instance
        inv = invert.circuit_definition()  
        inv.a <= io.I
        io.O <= inv.O
```

## Statically Elaborated For Loops
Statically elaborated for loops are supported using the [ast_tools loop
unrolling macro](https://github.com/leonardt/ast_tools#loop-unrolling).
Here's an example:
```python
from ast_tools.passes import begin_rewrite, loop_unroll, end_rewrite

n = 4
@m.circuit.combinational
@end_rewrite()
@loop_unroll()
@begin_rewrite()
def logic(a: m.Bits[n]) -> m.Bits[n]:
    O = []
    for i in ast_tools.macros.unroll(range(n)):
        O.append(a[n - 1 - i])
    return m.bits(O, n)
```
which compiles to this magma circuit
```python
class logic(m.Circuit):
    IO = ['a', m.In(m.Bits[n]), 'O', m.Out(m.Bits[n])]

    @classmethod
    def definition(io):
        O_0 = []
        O_0.append(io.a[n - 1 - 0])
        O_0.append(io.a[n - 1 - 1])
        O_0.append(io.a[n - 1 - 2])
        O_0.append(io.a[n - 1 - 3])
        __magma_ssa_return_value_0 = m.bits(O_0, n)
        O = __magma_ssa_return_value_0
        m.wire(O, io.O)
```


# Sequential Circuit Definition
The `@m.circuit.sequential` decorator extends the `@m.circuit.combinational`
syntax with the ability to use Python's class system to describe stateful
circuits.

The basic pattern uses the `__init__` method to declare state, and a `__call__`
function that uses `@m.circuit.combinational` syntax to describe the transition
function from the current state to the next state, as well as a function from
the inputs to the outputs.  State is referenced using the first argument `self`
and is implicitly updated by writing to attributes of self (e.g. `self.x = 3`).

Here's an example of a basic 2 element shift register:
```python
@m.circuit.sequential(async_reset=True)
class DelayBy2:
    def __init__(self):
        self.x: m.Bits[2] = m.bits(0, 2)
        self.y: m.Bits[2] = m.bits(0, 2)

    def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
        O = self.y
        self.y = self.x
        self.x = I
        return O
```

In the `__init__` method, the circuit declares two state elements `self.x` and
`self.y`.  Both are annotated with a type `m.Bits[2]` and initialized with a
value `m.bits(0, 2)`.  The `__call__` method accepts an input `I` with the same
type as the state elements. It stores the current value of `self.y` in
a temporary variable `O`, sets `self.y` to be the value of `self.x`, sets
`self.x` to be the input value `I` and returns `O`.  Notice that the inputs and
output of the `__call__` method have type annotations just like
`m.circuit.combinational` functions.  The `__call__` method should be treated
as a standard `@m.circuit.combinational` function, with the special parameter
`self` that provides access to the state.

The sequential syntax is implemented by compiling the above class definition
into a magma circuit definition instantiating the registers declared in the
`__init__` method and defining and wiring up a combinational function
corresponding to the `__call__` method.  The references to self attributes are
rewritten to be explicit arguments to the `__call__` method.  Here is the
output code for the above example:

```python
class DelayBy2(m.Circuit):
    IO = ['I', m.In(m.Bits[2]), 'CLK', m.In(m.Clock), 'ASYNCRESET', m.
        In(m.AsyncReset), 'O', m.Out(m.Bits[2])]

    @classmethod
    def definition(io):
        x = DefineRegister(2, init=0, has_async_reset=True)()
        y = DefineRegister(2, init=0, has_async_reset=True)()

        @combinational
        def DelayBy2_comb(I: m.Bits[2], self_x_O: m.Bits[2], self_y_O:
            m.Bits[2]) ->(m.Bits[2], m.Bits[2], m.Bits[2]):
            O = self_y_O
            self_y_I = self_x_O
            self_x_I = I
            return self_x_I, self_y_I, O
        comb_out = DelayBy2_comb(io.I, x, y)
        x.I <= comb_out[0]
        y.I <= comb_out[1]
        io.O <= comb_out[2]
```

## Hierarchy
Besides declaring magma values as state, the `sequential` syntax also supports
using instances of other sequential circuits.  For example, suppose we have a 
register defined as follows:

```python
@m.circuit.sequential(async_reset=True)
class Register:
    def __init__(self):
        self.value: m.Bits[2] = m.bits(init, 2)

    def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
        O = self.value
        self.value = I
        return O
```

We can use the `Register` class in the definition of a `ShiftRegister` class:

```python
@m.circuit.sequential(async_reset=True)
class TestShiftRegister:
    def __init__(self):
        self.x: Register = Register()
        self.y: Register = Register()

    def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
        x_prev = self.x(I)
        y_prev = self.y(x_prev)
        return y_prev
```

Notice that we annotate the type of the attribute with the class (sequential
circuit definition) and we initialize it with an instance of the class.  Then,
the attribute can be called with inputs to return the outputs. This corresponds
to calling the `__call__` method of the sub instance.

**NOTE** Currently it is required that every sub
sequential circuit element receive an explicit invocation in the `__call__`
method. For example, if you have a sub sequential circuit `self.x` that you
would like to keep constant, you must still call it with `self.x(...)` to
ensure that some input value is provided every cycle (the sub sequential
circuit must similarly be designed in such a way that the logic expects inputs
every cycle, so enable logic must be explicitly defined).

## Experimental: Direct to Verilog Compilation
Note: This feature requires the kratos package (install with `pip install kratos`)

`@combinational_to_verilog` and `@sequential_to_verilog` decorators provide
support for an alternative compiler that passes `if` statements down to verilog
and uses an `always_ff` block to implement the sequential registers.

For example,
```python
@m.circuit.combinational_to_verilog
def execute_alu(a: m.UInt[16], b: m.UInt[16], config_: m.Bits[2]) -> \
        m.UInt[16]:
    if config_ == m.bits(0, 2):
        c = a + b
    elif config_ == m.bits(1, 2):
        c = a - b
    elif config_ == m.bits(2, 2):
        c = a * b
    else:
        c = m.bits(0, 16)
    return c
```

compiles to
```verilog
module execute_alu (
  output logic [15:0] O,
  input logic [15:0] a,
  input logic [15:0] b,
  input logic [1:0] config_
);

logic [15:0] c;
always_comb begin
  unique case (config_)
    2'h0: c = a + b;
    2'h1: c = a - b;
    2'h2: c = a * b;
    default: c = 16'h0;
  endcase
  O = c;
end
endmodule   // execute_alu
```

and
```python
@m.circuit.sequential_to_verilog(async_reset=True)
class TestBasic:
    def __init__(self):
        self.x: m.Bits[2] = m.bits(0, 2)
        self.y: m.Bits[2] = m.bits(0, 2)

    def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
        _O = self.y
        self.y = self.x
        self.x = I
        return _O
```
compiles to
```verilog
module TestBasic (
  input logic ASYNCRESET,
  input logic CLK,
  input logic [1:0] I,
  output logic [1:0] O
);

logic [1:0] _O;
logic [1:0] self_x_I;
logic [1:0] self_x_O;
logic [1:0] self_y_I;
logic [1:0] self_y_O;

always_ff @(posedge CLK, posedge ASYNCRESET) begin
  if (ASYNCRESET) begin
    self_x_O <= 2'h0;
    self_y_O <= 2'h0;
  end
  else begin
    self_x_O <= self_x_I;
    self_y_O <= self_y_I;
  end
end
always_comb begin
  _O = self_y_O;
  self_y_I = self_x_O;
  self_x_I = I;
  O = _O;
end
endmodule   // TestBasic
```
