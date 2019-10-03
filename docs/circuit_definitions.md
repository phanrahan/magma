# Combinational Circuit Definitions
The `@m.circuit.combinational` decorator provides a way to use function syntax
for describing combinational circuits.  Inputs are given names and annotated
with a Magma type using Python 3's type annotation syntax.  Output type(s) are
provided using Python 3's return annotation syntax (`->`).  If a single output
type is specified, the magma circuit will have a single output named `O`.  If
`n` types are specified separated by commas, the magma circuit will have `n`
outputs named `O{i}` where `i` is the index of the type in the annotation.
Inside the combinational function, circuits can be described using control
flow, specifically `if` statements and `return` statements.  These constructs
will be compiled by magma using an SSA transformation pass, that turns `if`
statements into `phi` nodes that are equivalent to hardware muxes.  This
essentially allows the user to define muxes using if statements instead of
structural muxes.  All other code is untouched and will be passed through to
the normal downstream magma compiler, so things like instantiating another
magma circuit or basic for loops will work.

### Limitations
Because `if` statements are subject to the SSA transformation passes, normal
Python `if` statements (e.g. dispatching on a parameter) to a circuit generator
are not supported.  All `if` statements are treated as if they correspond to
hardware mux.  Support for the use of both Python `if`s and Magma `if`s is
forthcoming.

This feature is currently experimental, and therefor expect bugs to occur.
Please file any issues on the magma GitHub repository.

## If and Ternary
The condition must be an expression that evaluates to a `magma` value.

Basic example:
```python
@m.circuit.combinational
def basic_if(I: m.Bits(2), S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]

```

Basic nesting:
```python
class IfStatementNested(m.Circuit):
@m.circuit.combinational
def if_statement_nested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
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
def ternary(I: m.Bits(2), S: m.Bit) -> m.Bit:
    return I[0] if S else I[1]
```

Nesting terneray expressions
```python
@m.circuit.combinational
def ternary_nested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
    return I[0] if S[0] else I[1] if S[1] else I[2]
```

## Function composition:
```
@m.circuit.combinational
def basic_if_function_call(I: m.Bits(2), S: m.Bit) -> m.Bit:
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
def return_py_tuple(I: m.Bits(2)) -> (m.Bit, m.Bit):
    return I[0], I[1]
```

The other method is to use an `m.Tuple` (magma's tuple type).  Again, this is
specified in the type signature, using `m.Tuple(m.Type, m.Type, ...)`.  You can
also use the namedtuple pattern to give your multiple outputs explicit names
with `m.Tuple(O0=m.Bit, O1=m.Bit)`.


```python
@m.circuit.combinational
def return_magma_tuple(I: m.Bits(2)) -> m.Tuple(m.Bit, m.Bit):
    return m.tuple_([I[0], I[1]])
```

```
def return_magma_named_tuple(I: m.Bits(2)) -> m.Tuple(x=m.Bit, y=m.Bit):
    return m.namedtuple(x=I[0], y=I[1])
```

## Basic for loops
Basic for loops ranging over integer values are supported (they are ignored by
the syntax transformations so they will be executed as standard Python/magma
code). However, `if` statements are subject to an `ssa` transformation, so
they use the above described form (you can only assign to values inside an if
statement).

This code:
```python
n = 4
@m.circuit.combinational
def logic(a: m.Bits[n]) -> m.Bits[n]:
    O = []
    for i in range(n):
        O.append(a[n - 1 - i])
    return m.bits(O, n)
```

compiles to this magma circuit
```python
class logic(m.Circuit):
    IO = ['a', m.In(m.Bits[n]), 'O', m.Out(m.Bits[n])]

    @classmethod
    def definition(io):
        O_0 = []
        for i_0 in range(n):
            O_0.append(io.a[n - 1 - i_0])
        __magma_ssa_return_value_0 = m.bits(O_0, n)
        O = __magma_ssa_return_value_0
        m.wire(O, io.O)
```

which produces this verilog
```python
module logic (input [3:0] a, output [3:0] O);
assign O = {a[0],a[1],a[2],a[3]};
endmodule
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
atemporary variable `O`, sets `self.y` to be the value of `self.x`, sets
`self.x` to be the input value `I` and returns `O`.  Notice that the inputs and
output of the `__call__` method have type annotations just like
`m.circuit.combinational` functions.  The `__call__` method should be treated
as a standard `@m.circuit.combinational` function, with the special parameter
`self` that provides access to the state.

**NOTE** Currently it is required that every state element receive an explicit
value in the `__call__` method. For example, if you have a variable `self.x`
that you would like to keep constant, you must still assign it with `self.x =
self.x`.  Support for optional updates (implicit enable logic on the state) is
forthcoming (tracked by this issue
https://github.com/phanrahan/magma/issues/432).

## Hierarchy
Besides declaring magma values as state, the `sequential` syntax also supports
using instances of other sequential circuits.  For example, suppose we have a 
register defined as follows:

```python
@m.circuit.sequential(async_reset=True)
class Register:
    def __init__(self):
        self.value: m.Bits[width] = m.bits(init, width)

    def __call__(self, I: m.Bits[width]) -> m.Bits[width]:
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

**NOTE** Similarly to state elements, currently it is required that every sub
sequential circuit element receive an explicit invocation in the `__call__`
method. For example, if you have a sub sequential circuit `self.x` that you
would like to keep constant, you must still call it with `self.x(...)` to
ensure that some input value is provided every cycle (the sub sequential
circuit must similarly be designed in such a way that the logic expects inputs
every cycle, so enable logic must be explicitly defined).  Support for optional
calls (implicit enable logic on the state of the sub sequential circuit) is
forthcoming (tracked by this issue
https://github.com/phanrahan/magma/issues/432).
