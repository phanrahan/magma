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
- ~~Multiply `*`~~ Unsupported because mantle lacks an implementation, pull request welcome!
- ~~Divide `/`~~ Unsupported because mantle lacks an implementation, pull request welcome!
- Less than `<`
- Less than or equal `<=`
- Greater than `>`
- Greater than or equal `>=`

Note that the the right shift operator when applied to an `SInt` becomes
an arithmetic shift right operator (which replicates the sign bit as it shifts right).
