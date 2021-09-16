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
    inv.a @= io.I
    io.O @= inv.O
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

## Inline Combinational
`inline_combinational` avoids having to define function parameters, pass
arguments, and assign return values when defining a combinational block.  Instead,
the user can define a `combinational` function inside their `m.Circuit` class
defintiion and refer directly to magma values in the scope.  

Here's a simple example:

```python
class Main(m.Circuit):
    io = m.IO(invert=m.In(m.Bit), O0=m.Out(m.Bit), O1=m.Out(m.Bit))
    io += m.ClockIO()
    reg = m.Register(m.Bit)()

    O1 = m.Bit()

    @m.inline_combinational()
    def logic():
        if io.invert:
            reg.I @= ~reg.O
            O1 @= ~reg.O
        else:
            reg.I @= reg.O
            O1 @= reg.O

    io.O0 @= reg.O
    io.O1 @= O1
```

Notice that the first 3 lines of `Main`'s definition are standard magma.

Inside the function `logic` that has been decorated with
`@m.inline_combinational`, the user can refer to `reg` (a normal magma
instance) and it's ports to perform logic and wiring.  The definition of
`logic` shows two ways to use the `combinational` rewrite to generate a muxes.

The first way wires to `reg.I` using the `@=` operator inside the if statement.
The `combinational` rewrite logic will change these statements to assign to a
temporary value, which will then get process by the SSA pass to produce the
final value (output of a mux or chain of muxes) which is then wired to the
original target (`reg.I` in this case).

The second way assigns to a temporary value `O1`.  This value is handled using
the standard `combinational` treatment and the final value produced by SSA is
returned from the function and assigned in the enclosing environment.

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

    def __call__(self, en: m.Bit) -> m.SInt[16]:
        if en:
            self.count = self.count + 1
        return self.count.prev()
```

In the `__init__` method, the circuit declares a state element `self.count` as
an instance of the `m.Register` primitive.  The type is determined by the `T`
parameter to the Register circuit generator.  The `__call__` method accepts an
input `en` of type `m.Bit` that controls whether the state should be changed by
incrementing the value stored in the count register.  The output of the circuit
is returned, in this case `self.count.prev()`.  The `prev` method is a magic
method that will return the previous value of the count register (not the
updated value which could be `self.count + 1` is `en` is high).
Notice that the inputs and output of the `__call__` method have type
annotations just like `m.combinational2` functions.  The `__call__`
method should be treated as a standard `@m.combinational2` function,
with the special parameter `self` that provides access to the state declared
inside the `__init__` method.

### Hierarchy
Besides declaring magma values as state, the `sequential` syntax also supports
using instances of other sequential circuits.  For example, suppose we have a 
register defined as follows:

```python
@m.sequential2(reset_type=m.AsyncReset)
class Register:
    def __init__(self):
        self.value = m.Register(T=m.Bits[2], init=m.uint(0, 16))()

    def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
        return self.value(I)
```

We can use the `Register` class in the definition of a `ShiftRegister` class:

```python
@m.sequential2(reset_type=m.AsyncReset)
class TestShiftRegister:
    def __init__(self):
        self.x = Register()
        self.y = Register()

    def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
        return self.y(self.x(I))
```

**NOTE** Currently it is required that every sub
sequential circuit element receive an explicit invocation in the `__call__`
method. For example, if you have a sub sequential circuit `self.x` that you
would like to keep constant, you must still call it with `self.x(...)` to
ensure that some input value is provided every cycle (the sub sequential
circuit must similarly be designed in such a way that the logic expects inputs
every cycle, so enable logic must be explicitly defined).

## Coroutine
The `m.coroutine` syntax extends `m.sequential2` with the ability to use
`yield` statements inside the `__call__` method to pause execution and wait
until the next clock cycle.  This provides a convenient way to describe control
logic, particularly finite state machines.

Here's a simple example of defining a `UART` transmitter:
```python
@m.coroutine(reset_type=m.AsyncReset)
class UART:
    def __init__(self):
        self.message = m.Register(T=m.Bits[8], init=0)()
        self.i = m.Register(T=m.UInt[3], init=7)()
        self.tx = m.Register(T=m.Bit, init=1)()

    def __call__(self, run: m.Bit, message: m.Bits[8]) -> m.Bit:
        while True:
            self.tx = m.bit(1)  # end bit or idle
            yield self.tx.prev()
            if run:
                self.message = message
                self.tx = m.bit(0)  # start bit
                yield self.tx.prev()
                while True:
                    self.i = self.i - 1
                    self.tx = self.message[self.i.prev()]
                    yield self.tx.prev()
                    if self.i == 7:
                        break
```

In some cases, the user may desire to explicitly choose the encoding of each
state (by default, the compielr will generate a unique value for each `yield`
statement).  The coroutine syntax also supports `yield from` as a way to sequentially transfer
control to another coroutine.  This allows sequential composition of coroutines
(state machines). Here's an example of both in a JTAG controller:

```python
TEST_LOGIC_RESET = m.bits(15, 4)
RUN_TEST_IDLE = m.bits(12, 4)
SELECT_DR_SCAN = m.bits(7, 4)
CAPTURE_DR = m.bits(6, 4)
SHIFT_DR = m.bits(2, 4)
EXIT1_DR = m.bits(1, 4)
PAUSE_DR = m.bits(3, 4)
EXIT2_DR = m.bits(0, 4)
UPDATE_DR = m.bits(5, 4)
SELECT_IR_SCAN = m.bits(4, 4)
CAPTURE_IR = m.bits(14, 4)
SHIFT_IR = m.bits(10, 4)
EXIT1_IR = m.bits(9, 4)
PAUSE_IR = m.bits(11, 4)
EXIT2_IR = m.bits(8, 4)
UPDATE_IR = m.bits(13, 4)

@m.coroutine(manual_encoding=True, reset_type=m.AsyncReset)
class JTAG:
    def __init__(self):
        self.yield_state = m.Register(T=m.Bits[4], init=TEST_LOGIC_RESET)()

    def __call__(self, tms: m.Bit) -> m.Bits[4]:
        # TODO: Prune infeasible paths (or check if synthesis optimizes
        # them out)
        while True:
            while True:
                self.yield_state = TEST_LOGIC_RESET
                yield self.yield_state.prev()
                if tms == 0:
                    break
            while tms == 0:
                self.yield_state = RUN_TEST_IDLE
                yield self.yield_state.prev()
            while tms == 1:
                self.yield_state = SELECT_DR_SCAN
                yield self.yield_state.prev()
                if tms == 0:
                    # dr
                    yield from self.make_scan(CAPTURE_DR, SHIFT_DR,
                                              EXIT1_DR, PAUSE_DR, EXIT2_DR,
                                              UPDATE_DR)
                else:
                    self.yield_state = SELECT_IR_SCAN
                    yield self.yield_state.prev()
                    if tms == 0:
                        # ir
                        yield from self.make_scan(CAPTURE_IR, SHIFT_IR,
                                                  EXIT1_IR, PAUSE_IR,
                                                  EXIT2_IR, UPDATE_IR)
                    else:
                        break

    def make_scan(self, capture, shift, exit_1, pause, exit_2, update):
        def scan(self, tms: m.Bit) -> m.Bits[4]:
            self.yield_state = capture
            yield self.yield_state.prev()
            while True:
                if tms == 0:
                    while True:
                        self.yield_state = shift
                        yield self.yield_state.prev()
                        if tms != 0:
                            break
                self.yield_state = exit_1
                yield self.yield_state.prev()
                if tms == 0:
                    while True:
                        self.yield_state = pause
                        yield self.yield_state.prev()
                        if tms != 0:
                            break
                    self.yield_state = exit_2
                    yield self.yield_state.prev()
                    if tms != 0:
                        break
                else:
                    break
            self.yield_state = update
            yield self.yield_state.prev()
            return tms
        return scan()
```

Here's another example of `manual_encoding` and `yield from` in an SDRAM
controller:

```python
INIT_NOP1 = m.bits(0b01000, 5)
INIT_PRE1 = m.bits(0b01001, 5)
INIT_NOP1_1 = m.bits(0b00101, 5)
INIT_REF1 = m.bits(0b01010, 5)
INIT_NOP2 = m.bits(0b01011, 5)
INIT_REF2 = m.bits(0b01100, 5)
INIT_NOP3 = m.bits(0b01101, 5)
INIT_LOAD = m.bits(0b01110, 5)
INIT_NOP4 = m.bits(0b01111, 5)

REF_PRE = m.bits(0b00001, 5)
REF_NOP1 = m.bits(0b00010, 5)
REF_REF = m.bits(0b00011, 5)
REF_NOP2 = m.bits(0b00100, 5)

READ_ACT = m.bits(0b10000, 5)
READ_NOP1 = m.bits(0b10001, 5)
READ_CAS = m.bits(0b10010, 5)
READ_NOP2 = m.bits(0b10011, 5)
READ_READ = m.bits(0b10100, 5)

WRIT_ACT = m.bits(0b11000, 5)
WRIT_NOP1 = m.bits(0b11001, 5)
WRIT_CAS = m.bits(0b11010, 5)
WRIT_NOP2 = m.bits(0b11011, 5)

CMD_PALL = m.bits(0b10010001, 8)
CMD_REF = m.bits(0b10001000, 8)
CMD_NOP = m.bits(0b10111000, 8)
CMD_MRS = m.bits(0b10000000, 8)
CMD_BACT = m.bits(0b10011000, 8)
CMD_READ = m.bits(0b10101001, 8)
CMD_WRIT = m.bits(0b10100001, 8)

@m.coroutine(manual_encoding=True, reset_type=m.AsyncResetN)
class SDRAMController:
    def __init__(self):
        self.yield_state = m.Register(T=m.Bits[5], init=INIT_NOP1)()
        self.command = m.Register(T=m.Bits[8], init=CMD_NOP)()
        self.i = m.Register(T=m.UInt[4], init=m.uint(15, 4))()

    def __call__(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
        yield from self.init()
        while True:
            self.command = CMD_NOP
            self.yield_state = IDLE
            yield self.yield_state.prev(), self.command.prev()
            if refresh_cnt >= CYCLES_BETWEEN_REFRESH:
                yield from self.refresh()
            elif wr_enable:
                yield from self.write()
            elif rd_enable:
                yield from self.read()

    def init(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
        while True:
            self.command = CMD_NOP
            self.yield_state = INIT_NOP1
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        self.command = CMD_PALL
        self.yield_state = INIT_PRE1
        yield self.yield_state.prev(), self.command.prev()
        self.command = CMD_NOP
        self.yield_state = INIT_NOP1_1
        yield self.yield_state.prev(), self.command.prev()
        self.command = CMD_REF
        self.yield_state = INIT_REF1
        yield self.yield_state.prev(), self.command.prev()
        self.i = 7
        while True:
            self.command = CMD_NOP
            self.yield_state = INIT_NOP2
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        self.command = CMD_REF
        self.yield_state = INIT_REF2
        yield self.yield_state.prev(), self.command.prev()
        self.i = 7
        while True:
            self.command = CMD_NOP
            self.yield_state = INIT_NOP3
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        self.command = CMD_MRS
        self.yield_state = INIT_LOAD
        yield self.yield_state.prev(), self.command.prev()
        self.i = 1
        while True:
            self.command = CMD_NOP
            self.yield_state = INIT_NOP4
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        return refresh_cnt, rd_enable, wr_enable

    def refresh(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
        self.command = CMD_PALL
        self.yield_state = REF_PRE
        yield self.yield_state.prev(), self.command.prev()
        self.command = CMD_NOP
        self.yield_state = REF_NOP1
        yield self.yield_state.prev(), self.command.prev()
        self.command = CMD_REF
        self.yield_state = REF_REF
        yield self.yield_state.prev(), self.command.prev()
        self.i = 7
        while True:
            self.command = CMD_NOP
            self.yield_state = REF_NOP2
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        return refresh_cnt, rd_enable, wr_enable

    def write(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
        self.command = CMD_BACT
        self.yield_state = WRIT_ACT
        yield self.yield_state.prev(), self.command.prev()
        self.i = 1
        while True:
            self.command = CMD_NOP
            self.yield_state = WRIT_NOP1
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        self.command = CMD_WRIT
        self.yield_state = WRIT_CAS
        yield self.yield_state.prev(), self.command.prev()
        self.i = 1
        while True:
            self.command = CMD_NOP
            self.yield_state = WRIT_NOP2
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        return refresh_cnt, rd_enable, wr_enable

    def read(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
        self.command = CMD_BACT
        self.yield_state = READ_ACT
        yield self.yield_state.prev(), self.command.prev()
        self.i = 1
        while True:
            self.command = CMD_NOP
            self.yield_state = READ_NOP1
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        self.command = CMD_READ
        self.yield_state = READ_CAS
        yield self.yield_state.prev(), self.command.prev()
        self.i = 1
        while True:
            self.command = CMD_NOP
            self.yield_state = READ_NOP2
            yield self.yield_state.prev(), self.command.prev()
            if self.i == 0:
                break
            self.i = self.i - 1
        self.command = CMD_NOP
        self.yield_state = READ_READ
        yield self.yield_state.prev(), self.command.prev()
        return refresh_cnt, rd_enable, wr_enable
```
