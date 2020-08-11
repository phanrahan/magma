# Syntaxes
Magma's core syntax is at the structural RTL of abstraction.  Magma provides
layers on top of this core syntax to abstract some details such as wiring of
inputs/outputs, referencing registers, and control logic state machines.

## Core
Circuits are defined by subclassing `m.Circuit` and assigning an interface
definition to the variable named `io`.  Inside, the user creates instances of
other circuits and wires their ports to the `io` object.

```python
class Accum(m.Circuit):
        # Interface contains an input port and output port, both of type
        UInt[8]
        io = m.IO(
            I=m.In(m.UInt[8]),
            O=m.Out(m.UInt[8]))
        )
        # Add magma's standard clock interface (equivalent to
        # including CLK=m.In(m.Clock) in an m.IO call
        # Note that io objects can be incrementally constructed using the `+`
        # operator
        io += m.ClockIO()
        # Generate a register circuit that stores a value of type UInt[8] 
        # Second set of parenthesis instances the generated circuit
        sum = m.Register(m.UInt[8])()
        # Calling an instance `sum(...)` corresponds to wiring up the inputs
        # @= operator wires the output of sum (returned from calling the
        # instance) to the `O` port of the output
        io.O @= sum(sum.O + io.I)
        # Register clock signal is automatically wired up
```
## Combinational
Magma supports generating combinational logic from pure functions using the
`@m.combinational2` decorator.  This introduces a set of syntax level features
for defining combinational magma circuits, including the use of `if` statements
to generate `Mux`es.

The condition must be an expression that evaluates to a `magma` value.

Here's a simple example:
```python
@m.combinational2
def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]

```

For reference, here is the code produced for the corresponding magma circuit
definition where the if statement has been lowered into a multiplexer:
```python
class basic_if(m.Circuit):
    io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(Bit))
    Mux2xOutBit_inst0 = Mux2xOutBit()
    wire(io.I[1], Mux2xOutBit_inst0.I0)
    wire(io.I[0], Mux2xOutBit_inst0.I1)
    wire(io.S, Mux2xOutBit_inst0.S)
    wire(Mux2xOutBit_inst0.O, io.O)
```

`combinational2` allows nesting `if` statements:
```python
@m.combinational2
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

Also terneray expressions:
```python
@m.combinational2
def ternary(I: m.Bits[2], S: m.Bit) -> m.Bit:
    return I[0] if S else I[1]
```

### Function composition
```python
@m.combinational2
def basic_if_function_call(I: m.Bits[2], S: m.Bit) -> m.Bit:
    return basic_if(I, S)
```
Function calls must refer to another `m.combinational2` element, or a
function that accepts magma values, define instances and wires values, and
returns a magma.  Calling any other type of function has undefined behavior.

### Returning multiple values (tuples)

There are two ways to return multiple values, first is to use a Python tuple.
This is specified in the type signature as `(m.Type, m.Type, ...)`.  In the
body of the definition, the values can be returned using the standard Python
tuple syntax.  The circuit defined with a Python tuple as an output type will
default to the naming convetion `O0, O1, ...` for the output ports.

```python
@m.combinational2
def return_py_tuple(I: m.Bits[2]) -> (m.Bit, m.Bit):
    return I[0], I[1]
```

The other method is to use an `m.Tuple` (magma's tuple type).  Again, this is
specified in the type signature, using `m.Tuple(m.Type, m.Type, ...)`.  You can
also use the namedtuple pattern to give your multiple outputs explicit names
with `m.Tuple(O0=m.Bit, O1=m.Bit)`.


```python
@m.combinational2
def return_magma_tuple(I: m.Bits[2]) -> m.Tuple[m.Bit, m.Bit]:
    return m.tuple_([I[0], I[1]])
```

```python
@m.combinational2
def return_magma_named_tuple(I: m.Bits[2]) -> m.Product.from_fields("anon", {"x": m.Bit, "y": m.Bit}):
    return m.namedtuple(x=I[0], y=I[1])
```

### Using non-combinational magma circuits
The combinational syntax allows the use of other combinational circuits using
the function call syntax to wire inputs and retrieve outputs.

Here is an example:
```python
class EQ(m.Circuit):
    IO = ["I0", m.In(m.Bit), "I1", m.In(m.Bit), "O", m.Out(m.Bit)]

@m.combinational2
def logic(a: m.Bit) -> (m.Bit,):
    if EQ()(a, m.bit(0)):
        c = m.bit(1)
    else:
        c = m.bit(0)
    return (c,)
```

### Using magma's higher order circuits
```python
class Not(m.Circuit):
    IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

@m.combinational2
def logic(a: m.Bits[10]) -> m.Bits[10]:
    return m.join(m.map_(Not, 10))(a)
```

### Using combinational circuits as a standard circuit definition
Combinational circuits can also be used as standard circuit definitions by
using the `.circuit_definition` attribute to retrieve the corresponding magma
circuit.
```python
@m.combinational2
def invert(a: m.Bit) -> m.Bit:
    return Not()(a)

class Foo(m.Circuit):
    IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

    # reference circuit_definition and instance
    inv = invert.circuit_definition()  
    inv.a <= io.I
    io.O <= inv.O
```

### Statically Elaborated For Loops
Statically elaborated for loops are supported using the [ast_tools loop
unrolling macro](https://github.com/leonardt/ast_tools#loop-unrolling).
Here's an example:
```python
from ast_tools.passes import loop_unroll, apply_ast_passes

n = 4
@m.combinational2
@apply_ast_passes([loop_unroll()])
def logic(a: m.Bits[n]) -> m.Bits[n]:
    O = []
    for i in ast_tools.macros.unroll(range(n)):
        O.append(a[n - 1 - i])
    return m.bits(O, n)
```
which compiles to this magma circuit
```python
class logic(m.Circuit):
    io = m.IO(a=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))

    O_0 = []
    O_0.append(io.a[n - 1 - 0])
    O_0.append(io.a[n - 1 - 1])
    O_0.append(io.a[n - 1 - 2])
    O_0.append(io.a[n - 1 - 3])
    __magma_ssa_return_value_0 = m.bits(O_0, n)
    O = __magma_ssa_return_value_0
    m.wire(O, io.O)
```


## Sequential
The `@m.sequential2` decorator extends the `@m.combinational2`
syntax with the ability to use Python's class system to describe stateful
circuits.

The execution of `sequential` clases begins with the `__init__` method where
arbitrary magma code can be run to construct the internal state of a circuit.
Then, the `__call__` function constructs the state transition logic as well as
the input/output logic using `@m.combinational2` syntax.
State is referenced using the first argument `self` and is implicitly updated
by writing to attributes of self (e.g. `self.x = 3`).

Here's an example of a basic 2 element shift register:
```python
@m.sequential2()
class Counter:
    def __init__(self, reset_type=m.AsyncReset, has_enable=True):
        # reset_type and has_enable will be set implicitly
        self.count = m.Register(T=m.UInt[16], init=m.uint(0, 16))()

    def __call__(self) -> m.SInt[16]:
        self.count = self.count + 1
        return self.count
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

## Coroutine
