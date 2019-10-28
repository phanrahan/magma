## Operators

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

### Verilog Users Guide

Here we provide a mapping between Verilog's standard operators, as defined by
[IEEE Std 1800-2017: IEEE Standard for SystemVerilog—Unified Hardware Design,
Specification, and Verification
Language](https://ieeexplore.ieee.org/document/8299595) (page 256, Table 11-1
-- Operators and data types).

#### Assignment
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `=`              | `m.wire`, `<=` (can only be used on magma input values) | Any | All | Assignment cannot be overloaded for arbitrary Python variables, so in general we must use `m.wire`. We have added preliminary for assignment to attributes of magma values using the `<=` operator, which may be familiar for Verilog programmers using non-blocking assignments. Example: `reg.I <= io.I`.  `<=` is purely syntactic sugar defiend on output values and calls `m.wire` under the hood. |
| `+=`, `-=`, `/=`, `*=` | `None`   | None  | All     | Support is not planned for these operators because magma cannot provide a clean semantics for them.  Assignment only works for inputs to circuit instances and outputs of circuit definitions.  AugAssign operators imply a value that is used both as an input an output. For example, `inst.a +=1` would imply a is an output that feeds into binary add with 1, while also an input which consumes the result of the binary add. |
| `%=` | `None` | None | All | See above |
| `&=`, `\|=`, `^=` | `None` | None | All | See above |
| `>>=`, `<<=` | `None` | None | All | See above |
| `>>>=`, `<<<=` | `None` | None | All | See above |

#### Conditional Operator
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `?:`              | `<true_exp> if <cond> else <false_exp>`       | `true_exp : T`, `cond_exp : Bit`,  `false_exp : T`    | `m.circuit.combinational`     | Currently only supported inside the `m.circuit.combinational` syntax because it requires inspection of the AST and rewriting it into a `Mux`. The true expression and the false expression should have the same type, the condition expression should have a Bit type. |
| `?:`              | `mantle.mux([<false_exp>, <true_exp>], <cond>)`       | `true_exp : T`, `cond_exp : Bit`,  `false_exp : T`    | All     |  |

#### Unary Logical Operators
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `!`                | **TODO**         | `m.Bit`, `m.Bits` |  All | Logical operators like `not` cannot be overloaded in Python. Planned support for a mantle function `m.lnot` as an alternative |
| `~`, `&`, `~&`, `\|`, `~\|`, `^`, `~^`, `^~` | **TODO** | `m.Bits` | All | Python does not have built-in support for reduction operators. Use the python `reduce` function instead, e.g. `reduce(mantle.nand, value)`. |

#### Unary Arithmetic Operators
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `+`, `-` |  **TODO** | `m.SInt` | All | Can override `__neg__` and `__pos__` to implement these |
| `++`, `--` | None | None | All | No planned support since not available in Python, use `+= 1` and `-= 1` instead. |

#### Binary Logical Operators
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `<<`, `>>`       | `<<`, `>>`     | `m.Bits` | All | **TODO: What does verilog expect for bit width of the shift value? What does magma expect?** |
| `&&`, `\|\|`     | **TODO**       | `m.Bits` | All | **NOTE** Python doesn't support overloading logical `and` and `or`, so using those Python operators will not work and will likely lead to difficult to debug error messages. In the future, will provide mantle functions instead and possibly an AST rewriter that translates these operators into the matnle function calls. |
| `->`, `<->`      | None       | None | All | Impliciation and equivalence are used for verification, no planned support. If we wanted, we could provide mantle functions taht implement them as `!expression1 || expression2` (implication) and `(!expression1 || expression2) && (!expression2 || expression1)` |
| `==`, `!=`       | `==`, `!=`     | All | All |  |

#### Binary Arithmetic Operators
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `+`, `-`, `*`, `/`, `**` | `+`, `-`, `*`, `/`, `**` | `UInt`, `SInt` | All | **TODO: Define numeric or integral type where UInt and SInt are sub types** |
| `%` | `UInt`, `SInt` | All | **TODO: Define numeric or integral type where UInt and SInt are sub types** |
| `>>>`, `<<<`     | `>>`, `<<` | `SInt` | All | Python does not provide a separate operator for arithmetic shift operators. Instead, we overload the meaning of the normal shift operators on `SInt` types. To use the logical variant, one can use the operator function directly `mantle.lsr` or convert the type to `Bits` or `UInt`. **TODO: Double check that these are properly defined for SInt**. Note, according to the SV spec, arithmetic left shift is the same as logical left shift. |

#### Concatenation and Replication Operators
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `{}`     | `m.concat`     | All   | All     | **NOTE:** The semantics of `m.concat` are inverted from Verilog's (in the same way that Magma/Python's slicing syntax is inverted), so `m.concat(x,y)` corresponds to Verilog code of `{y,x}` as opposed to `{x,y}`  |
| `{{}}`     | **TODO**     | All   | All     | **TODO: We could use something similar to Python's list replication syntax: `[4] * 4` |

#### Others
| Verilog Operator | Magma Operator | Types | Context | Comments |
|------------------|----------------| ----- | ------- | -------- |
| `===`, `!==`     | None | None | None | Magma currently does not support 4-state logic (`===` tests for 1, 0, z, and x) |
| `==?`, `!=?`     | None | None | None | See above (`==?` treat X and Z values in a given bit position as a wildcard (matches any value)) |
| `inside`         | None | None | None | **TODO: Could use Python's `in` syntax to implement this, but is this typically used in synthesized code?** |
| `dist`           | None | None | None | Verification feature used for constraints |
| `{<<{}}`, `{>>{}}` | None | None | None |  |
