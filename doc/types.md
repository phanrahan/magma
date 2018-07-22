## Magma Types and Values

Magma is a strongly typed language within python.
All Magma types are python classes.
Magma types are used to declare the interface to a Circuit.
Instances of Magma types are Magma values.
Instances of circuits contain an interface with Magma values.

The first major set of types are single bit types. 
They are subclasses of `_Bit`.
```python
class _Bit(Type):
  class Clock(_Bit):
  class Bit(_Bit):
```
The `Bit` type can be used in logical operations;
the `Clock type can only be wired to other clocks.

The second major type in Magma is the `Array` type.
An `Array` consists of `n` values of the same type `T`.
```python
Array(n, T)
```

The third major type in Magma is the `Tuple` type.
An `Tuple` consists of `n` named values of different types `Tn`.
```python
Tuple(name0, T0, name1, T1, …, namen, Tn)
```

The `Bits` type is equivalent to an array of `Bit`.
It is a subclass of an array type.
The `UInt` and `SInt` create unsigned and signed integer types.
`UInt` and `SInt` are subclasses of the `Bits` type.
`Bits`, `UInt`, and `SInt` are separate types because they support different operations.
```python
Bits(n) # ~= Array(n, Bit)
        # &, |, ^, ~, ==, <<, >>
SInt(n) # +, -, *, /, <, <=, >=, >, -, >>>
UInt(n) # +, -, *, /, <, <=, >=, >
```

`Array`, `Tuple`, `Bits`, `UInt`, and `SInt` (Type Constructors) are python functions
that return new python classes.
The classes returned are subclasses of the Magma class `Kind`, the abstract base class for all Magma types.
The `Bit` class is a subclass of `BitKind`;
the `Clock` class is a subclass of `ClockKind;
All constructed Array classes are subclasses of `ArrayKind`;
and so on.
Types can be tested for equality and inequality.

Values are instances of Magma classes.
All values are subclasses of the Magma type `Type`.
An instance of `Bit` is a subclass of `BitType`, 
and so on.

## Conversions

Conversions between values are performed with conversion functions.
The functions follow the standard python convention for converting values,
e.g. int(s,base) converts a string in the given base to an integer.

```python
# convert to a Bit value
bit(int|clock|Array(1,Bit)|Bits(1)|UInt(1)|SInt(1))

# convert to a Clock value
clock(int|bit|Array(1,Bit)|Bits(1)|UInt(1)|SInt(1))

# convert to an Array(n,T) value
array(int|bit|Bits(n)|UInt(n)|SInt(n)|[t0, t1, ..., tn])

# convert to Bits(n) value
bits(int|bit|Array(n,Bit)|UInt(n)|SInt(n)|[b0, b1, ..., bn])

# convert to an unsigned int UInt(n) value
uint(int|bit|Array(n,Bit)|Bits(n)|SInt(n)|[t0, b1, ..., bn])

# convert to a signed int SInt(n) value
sint(int|bit|Array(n,Bit)|Bits(n)|UInt(n)|[t0, b1, ..., bn])
```

## Operators

All types support the following operators:
- Equal `==`
- Not Equal `!=`

The `Bit` type supports the following logical operators.
- And `&` 
- Or `|` 
- Exclusive or `^` 
- Not `~`

The `Bits` type supports the following logical operators.
- And `&` 
- Or `|` 
- Exclusive or `^` 
- Not `~`
- Logical right shift (with zeros) `>>` 
- Logical left shift (with zeros) `<<`

The `UInt` and `SInt` types support all the logical operators
as well as arithmetic and comparison operastors.
- Add `+`
- Subtract `-`
- Multiply `*`
- Divide `/`
- Less than `<`
- Less than or equal `<=`
- Greater than `>`
- Greater than or equal `>=`

Note that the the right shift operator when applied to an `SInt` becomes 
an arithmetic shift right operator (which replicates the sign bit as it shifts right).

## Functions

Magma has many other utility functions.

```python
# concatenate Arrays, Bits, UInt, SInt.
concat(a0, a1, ...,an)

# form an array by repeat a complex value n times
# form a Bits by repeating a bit n times.
repeat(value, n)

# zero extend a Bits, UInt, SInt by n bits
zext(bits, n)

# sign extend a SInt by n bits
sext(sint, n)
```

## Mantle Primitives

Magma has built-in operators for combinational logic functions
including logical operators, arithmetic operators, and comparison operators.
It also builds in basic multiplexers.
Finally, registers and memories are defined as primitive circuits.

Additional circuits are provided in the
[Mantle](https://github.com/phanrahan/mantle) library.
These circuits include counters, shift register, and other useful functions.
Finally, the mantle library includes low-level device primitives for different FPGAs,
and efficient vendor-specific implementations of the standard Magma primitives.

- Combinational logic
  - [Logical Operators](https://github.com/phanrahan/mantle/blob/master/doc/logic.md)
  - [Arithmetic Operators](https://github.com/phanrahan/mantle/blob/master/doc/arith.md)
  - [Comparison Operators](https://github.com/phanrahan/mantle/blob/master/doc/compare.md)
  - [Multiplexers](https://github.com/phanrahan/mantle/blob/master/doc/mux.md)
  - [Decoders, Encoders, and Arbiters](https://github.com/phanrahan/mantle/blob/master/doc/decode.md)
- Sequential logic
  - [Flip-flops and Register](https://github.com/phanrahan/mantle/blob/master/doc/register.md)
  - [Counters](https://github.com/phanrahan/mantle/blob/master/doc/counter.md)
  - [Shift Registers](https://github.com/phanrahan/mantle/blob/master/doc/shift.md)
- [Memory](https://github.com/phanrahan/mantle/blob/master/doc/memory.md)

