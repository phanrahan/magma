# Types
* `Analog` - Base type for analog signals
* `Digital` - Base type for digital signals
* `Bit(Digital)` - Boolean
* `Clock(Digital)` - Clock
* `Reset(Digital)` - Synchronous Posedge Reset
* `ResetN(Digital)` - Synchronous Negedge Reset
* `AReset(Digital)` - Asynchronous Posedge Reset
* `AResetN(Digital)` - Asynchronous Negedge Reset
* `Enable(Digital)` - Enable
* `Array[N, T]` - Homogenous aggregate type of fixed length `N` containing
  members of type `T`
* `Tuple[T0, T1, ...]` - Heterogenous aggregate type mapping indices `0, 1, ...` to types `T0, T1, ...`
* `Product.from_fields("name", {"k0": T0, "k1": T1, ...})` - Heterogenous
  aggregate type mapping fields `k0, k1, ...` to types `T0, T1, ...`.
* `Sum[T0, T1, ...]` - Type that can be one of multiple types `T0, T1, ...`

**TODO**: Section on user defined types and introspecting types


# Circuits
**Defining:** subclass `m.Circuit` defines a 
```python
def DefineAccum(width: int):
    class Accum(m.Circuit):
        IO = m.IO(
            I=m.In(m.UInt[width]),
            O=m.Out(m.UInt[width]),
            # TODO: Automatically lift internal clock ports?
            **m.ClockInterface()
        )
        # Note: Currently mantle.Register accepts the width, but it will be
        # updated to accept a type corresponding to the value stored in the
        # register, which allows it to generalize over user defined types
        sum_ = mantle.Register(m.UInt[width])
        # Calling an instance corresponds to wiring up the inputs
        IO.O <= sum_(sum_.O + IO.I)
        # Register clock signal is automatically wired up
    return Accum
```

**TODO** Introspecting circuits

# Values and Wiring
Basic values are constructed as instances of magma types.  A set of magma values
are implicitly constructed when defining an interface (`IO`) object.

Values corresponding to input types may be used to drive an arbitrary
number of outputs, but may not be driven by any value.

Values corresponding to output types must be driven by exactly one source value.

Values corresponding to analog types, may be connected an arbitrary number 
of times to any other analog values.

```python
class Test(Circuit):
    IO = IO(
        I0=m.In(m.Bits[5]),
        I1=m.In(m.Bits[5]),
        O0=m.Out(m.Bits[5])
        O1=m.Out(m.Bits[5])
    )
    # Legal, wire input to output
    IO.O0 <= IO.I0

    # Illegal, cannot wire output to input
    IO.I1 <= io.O1

    # Legal, wire input to multiple outputs
    IO.O1 <= io.I0

    # Illegal, O0 already has a driver
    IO.O0 <= io.I1

    # Illegal, cannot wire input to input
    IO.I0 <= io.I1

```

Intermediate values are constructed by instancing a type.
At the end of a definition, an intermediate value must have exactly one value driving the
input but may be used to drive multiple outputs.
```python
class Test(Circuit):
    IO = IO(
        I=m.In(m.Bits[5]),
        O=m.Out(m.Bits[5])
    )

    x = Bits[5]()
    y = Bits[5]()
    y <= IO.I
    x <= y
    IO.O <= x
```

**TODO** Discuss value conversions
**TODO** Introspecting values

# Primitives
* `EQ`, `NEQ` - Check if two values are equal or not equal
* `And`, `Or`, `XOr`, `Not` - Bitwise logical operators defined on `Bit`,
  N-dimensional Array of `Bit`, and Tuples of `Bit`
* `Mux(I, S)` - where `len(S) == log2_ceil(len(I))` and the value of `S`
  corresponds to the index in `I` to be selected
* `LShift` - left shift defined on `Bits` and its subtypes
* `LRShift` - logical right shift defined on `Bits` and `UInt`
* `ARShift` - arithmetic right shift defined on `SInt`
* `Add`, `Sub`, `Negate`, `Multiply`, `Divide` - general arithmetic operations
  defined on `UInt` and `SInt`
* `ULT`, `ULE`, `UGT`, `UGE` - unsigned comparison operations defined on `UInt`
* `SLT`, `SLE`, `SGT`, `SGE` - signed comparison operations defined on `SInt`
* `AddE`, `SubE` - variants of add and subtract that extend the output widths
  to include a carry bit
* `UMulE`, `SMulE` - variants of multiply that extend the output widths to be
  the sum of the input widths
* `zext(arr, n)` - extend array value `n` zeros
* `sext(arr, n)` - extend array value with `n` copies of the MSB
* `concat(*arrays)` - concatenate multiple array values 
* `repeat(value, n)` - create an array replicating 
* `Register(T, init=0, has_ce=False, has_reset=False, reset_type=Reset)` -
  creates a `Register` of type `T` with optional parameters for clock enable
  (`has_ce`), reset (`has_reset`) and reset type (`reset_type`).
* `Memory(height, width, read_latency=0, num_read_ports=1, num_write_ports=1)`
  - `height` is the number of elements, `width` is the width of each element,
  `read_latency` is the number of cycles of delay before a read is available,
  `num_read_ports` specifies the number of read ports, `num_write_ports`
  specifies the number of write ports (can be 0 for a ROM)

# Operators
All types support the following operators:
- Equal `==`
- Not Equal `!=`

The `Bit` type supports the following logical operators.
- And `&`
- Or `|`
- Exclusive or `^`
- Not `~`

The `Array` type supports the following operator.
- Dynamic bit selection `bits_obj[add.O]` (select a bit dynamically using a magma value)

The `Bits` type supports the following logical operators.
- And `&` (elementwise)
- Or `|` (elementwise)
- Exclusive or `^` (elementwise)
- Not `~` (elementwise)
- Logical right shift (with zeros) `>>`
- Logical left shift (with zeros) `<<`

The `UInt` and `SInt` types support all the logical operators
as well as arithmetic and comparison operastors.
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

# Syntax Extensions
## Combinational
**TODO**
## Sequential
**TODO**
