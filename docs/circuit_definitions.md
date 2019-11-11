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
def return_magma_tuple(I: m.Bits[2]) -> m.Tuple(m.Bit, m.Bit):
    return m.tuple_([I[0], I[1]])
```

```python
@m.circuit.combinational
def return_magma_named_tuple(I: m.Bits[2]) -> m.Tuple(x=m.Bit, y=m.Bit):
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
        inv = invert.circuit_definition()
        inv.a <= io.I
        io.O <= inv.O
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
