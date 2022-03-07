**NOTE**: This is a work in progress, please let us know via issue/gitter/email
if you'd like to see anything added to this.

This is inspired by the [chisel cheatsheet](https://github.com/freechipsproject/chisel-cheatsheet)
and will be rendered in a similar single page layout soon.

# Types
## Bit
* `m.Bit`: boolean value
* `m.VCC, m.GND`: boolean literals

## Bits and Integers
* `m.Bits[N]`: length `N` bit vector with bitwise logical operators defined
* `m.UInt[N]`: length `N` unsigned integer that includes Bits operators and
  unsigned arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)
* `m.SInt[N]`: length `N` signed integer that includes Bits operators and
  signed arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)

## Array
* `m.Array[N, T]`: fixed length array of length `N` containing values of type
  `T` with equality operator (`==`) defined

## Tuples and Products
* `m.Tuple[t0, t1, ...]`: heterogenous compound data type containing members of
  type `t0`, `t1`, ... Values of such types can be indexed using integer keys
  like Python tuples (e.g. for a tuple value `x`, `type(x[0]) == t0`).
* `m.Product.from_fields(name, dict(k0=t0, k1=t1, ...))`: heterogenous compound
  data type containing members of type `t0`, `t1`, ... Values of such types can
  be indexed using attributes (e.g. for a product value `x`, `type(x.k0) ==
  t0`). `name="anon"` makes this type anonymous.
  * Alternate syntax:
  ```python
  class <name>(m.Product):
      k0 = t0
      k1 = t1
      ...
  ```

## Enum
Statically typed enumerated type:
```python
class <name>(m.Enum):
    k0 = v0
    k1 = v1
    ...
```

# Type qualifiers
`m.In(T)`, `m.Out(T)`, `m.InOut(T)` qualify type `T` to be an input, output, and
inout respectively.

# Type conversions
* `m.bits(value, n=None)`: convert `value` to an `Bits` (same rules as
  `m.array` except if the input is a magma type or list, the members must be
  convertible to a Bit (e.g. `Bit`, `bool`, `0`, `1`))
* `m.array(value, n=None)`: convert `value` to an array.  `value` must be a
  magma type (`Bit`, `Tuple`, `Array`), a Python integer (e.g. literal), or a Python
  sequence (e.g. list).  If `n` is `None`, the width of the array is inferred
  from `value` (e.g. length of the list, bit length of the integer, length of
  the magma type)
* `m.uint(value, n=None)`: convert `value` to an `UInt` (same rules as
  `m.bits`, except will not convert `m.SInt` to `m.UInt`)
* `m.sint(value, n=None)`: convert `value` to an `SInt` (same rules as
  `m.bits`, except will not convert `m.UInt` to `m.SInt`)

# Registers
Retain state until updated:
```python
my_reg = mantle.Register(32)
my_reg_init_7 = mantle.Register(32, init=7)
my_reg_clock_enable = mantle.Register(32, init=7, has_ce=True)
my_reg_uint = mantle.Register(32, init=7, has_ce=True, T=m.UInt)
```
Define update value by wiring to the input `I` port
```
my_reg.I @= next_val
```
Set `N` to `None` for a Register of a single `Bit` (setting `N` to `1` will
produce a register of `Bits[1]`)
```python
bit_reg = mantle.Register(None)
```

# Memories
```python
MyMemCircuit = mantle.DefineMemory(height, width, readonly=False, read_latency=0)
my_mem_inst = MyMemCircuit()
```
* `height`: number of elements
* `width`: width of each element
* `readonly`: ROM if True else RAM
* `read_latency`: number of registers to append to read out port

Memory ports (where `addr_width = max(clog2(height - 1), 1)`):

* `RADDR`: `m.In(m.Bits[addr_width])`
* `RDATA`: `m.Out(m.Bits[width])`
* `WADDR`: `m.In(m.Bits[addr_width])`
* `WDATA`: `m.In(m.Bits[width])`
* `CLK`: `m.In(m.Clock)`
* `WE`: `m.In(m.Bit)`

# Circuits
**Defining**: subclass `m.Circuit`
```python
class Accum16(m.Circuit):
    io = m.IO(I=m.In(m.UInt[16]), O=m.Out(m.UInt[16])) + m.ClockIO()

    sum_ = mantle.Register(16)
    io.O @= sum_(m.uint(sum_.O) + io.I)
```
**Usage**: circuits are used by instancing them inside another definitions and
  their ports are accessed using dot notation
```python
my_module = Accum16()
my_module.I @= some_data
sum_ = my_module.O
```

**Wiring**: wire an output to an input using `@=` operator (statically typed)

**Metaprogramming**: abstract over parameters by generating a circuit definition inside a closure
```python
def define_accum(width: int):

   class Accum(m.Circuit):
        name = f"Accum{width}"
        io = m.IO(I=m.In(m.UInt[width]), O=m.Out(m.UInt[width])) + m.ClockIO()

        sum_ = mantle.Register(width)
        io.O @= sum_(m.uint(sum_.O) + io.I)

   return Accum
```

# Operators
## Infix operators
All types support the following operators:
- Equal `==`
- Not Equal `!=`

The `Bit` type supports the following logical operators.
- And `&`
- Or `|`
- Exclusive or `^`
- Not `~`

The `Array` type family supports the following operator.
- Dynamic bit selection `my_arry[add.O]` (select a bit dynamically using a magma value).

The `Bits` type family supports the following logical operators.
- And `&` (element-wise)
- Or `|` (element-wise)
- Exclusive or `^` (element-wise)
- Not `~` (element-wise)
- Logical right shift (with zeros) `>>`
- Logical left shift (with zeros) `<<`

The `UInt` and `SInt` types support all the logical operators
as well as arithmetic and comparison operators.
- Add `+`
- Subtract/Negate `-`
- Multiply `*`
- Divide `/`
- Less than `<`
- Less than or equal `<=`
- Greater than `>`
- Greater than or equal `>=`

Note that the the right shift operator when applied to an `SInt` becomes
an arithmetic shift right operator (which replicates the sign bit as it shifts right).

## Functional operators
- `mantle.mux(*I, S)` (constraint: `len(S) == log2_ceil(len(I))`): select `I[S]`.
- `m.zext(v, n)`: zero extend array `v` by `n`
- `m.sext(v, n)`: sign extend array `v` by `n`
- `m.concat(*arrays)`: concat arrays together
- `m.repeat(value, n)`: create an array repeating `value` `n` times

# Combinational
```python
@m.circuit.combinational
def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]

```

produces

```python
basic_if = DefineCircuit("basic_if", "I", In(Bits[2]), "S", In(Bit), "O", Out(Bit))
Mux2xOutBit_inst0 = Mux2xOutBit()
wire(basic_if.I[1], Mux2xOutBit_inst0.I0)
wire(basic_if.I[0], Mux2xOutBit_inst0.I1)
wire(basic_if.S, Mux2xOutBit_inst0.S)
wire(Mux2xOutBit_inst0.O, basic_if.O)
EndCircuit()
```
See [here](circuit_definitions.md) for more details.

# Sequential
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
See [here](circuit_definitions.md) for more details.
