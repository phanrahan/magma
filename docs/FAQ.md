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
