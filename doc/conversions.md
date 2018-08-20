## Conversions

Conversions between `Magma` values are performed 
with `Magma` conversion functions.
The functions are named by following 
the standard python naming convention for converting values,
e.g. `int(s,base)` converts a string in the given base to an integer.

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
uint(int|bit|Array(n,Bit)|Bits(n)|SInt(n)|[b0, b1, ..., bn])

# convert to a signed int SInt(n) value
sint(int|bit|Array(n,Bit)|Bits(n)|UInt(n)|[b0, b1, ..., bn])
```
