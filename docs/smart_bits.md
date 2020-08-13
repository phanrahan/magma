# SmartBits

## Overview
"Smart" types in magma (`SmartBits`, `SmartBit`) emulate verilog bits types, allowing very compact syntax for describing datapaths. For example, we can simply write the following:

```python
x = m.smart.SmartBits[7]()
y = m.smart.SmartBits[9]()
z = m.smart.SmartBits[12]()

expr = (~(x + y) + z) << x

a @= expr
```

Note that using raw magma types (i.e. `Bits`, `UInt`, `SInt`), we would have to do several explicit extensions and explicit promotion to `UInt` (for example, because addition is not defined on plain `Bits`). The smart types allow for writing this simple syntax while still compiling to raw magma types (and therefore the generated code still adheres to the typing rules of the raw magma types).

It should also be noted that due to the implementation details, expressions on smart types are not actually operable magma types. In fact, the only thing you can do with them is wire them to other smart types, as in `a @= expr`. At the time of wiring, bit-widths and signedness of operands are resolved as a function of the expression itself and the left hand side of the assignment (see below for details). So, in the following code segment
    expr = ...
    a @= expr
    b @= expr
different RTL could be generated based on the bit-widths of `a` and `b`. As a corollary, it is evident that the same expression can be wired multiple times, making these expressions macro-like.

## Types
There are two smart type constructors:
* `SmartBits[<int>, <bool>]`: returns a SmartBits type with bit-width equal to the first argument and signedness equal to the second argument. The second argument (signedness) defaults to false; therefore `SmartBits[n, False]` is equivalent to `SmartBits[n]`.
* `SmartBit` which is a literal alias of `SmartBits[1]`.

Expressions built on top of these base smart types are of an intermediate type `SmartExpr`, which can only (a) be used in another expression, such as `dbl = expr + expr`, or (b) be on the right hand side of a wiring assignment. Besides these two operations (and calling `str()` for debugging), these intermediate objects are not meant to be introspected or operated on by the user.

## Operators
Arithmetic, bit-wise logical, comparison, shift, bit-wise reduction, and concat operators are defined for all smart types and intermediates. All operators are implemented as python-style infix operators (e.g. `a + b`), except for the following:
* Concat: the function `concat` is a free, variadic function; e.g. `long = concat(x, y, z)`
* Bit-wise reduce: bit-wise reductions are defined as a member function `reduce`, which takes the reduction operator as an argument; e.g. `short = x.reduce(operator.or_)`

See the end of the document for a table summarizing all operators.

## Inference
We first define a *partial expression* to be any (potentially compound) expression with smart operands, without wiring, and we define a *complete expression* to be any wiring statement where the left hand side is a base smart type and the right hand side is a partial expression. Every complete expression is dynamically resolved using a scheme to infer the bit-width and signedness of each operand. This is inspired from the [Verilog standard](https://www.eg.bucknell.edu/~csci320/2016-fall/wp-content/uploads/2015/08/verilog-std-1364-2005.pdf) (see Sec. 5.2).

In general, every partial expression appearing in a complete expression is either *self-determined* or *context-determined*. This distinguishes expressions which require the entirety of the complete expression in-order to do inference, or only the partial expression. Each operator may have further specialized inference rules.

### Bit-width
The rule of thumb for context-determined expressions is that all its operands get extended to the **longest** operand appearing in the complete expression (including the LHS of the assignment). On the other hand, the scope for self-determined expressions is only the partial expression itself. Note that since a context-determined expression can appear within a self-determined expression, each self-determined expression must still be processed by the inference step, except that the context is limited to just the expression itself, and in particular, the LHS of the assignment is excluded.

The bit-width of any partial expression's result is determined by the specific operator (see table below). For example the result of addition has bit-width equal to the maximum of all of its operand bit-widths, where as the result of comparison always has bit-width equal to 1.

### Signedness
The signedness of operands can both determine the semantics of operators, as well as how operands are extended. For example, signed-comparison has different semantics than unsigned-comparison, and operands can either be sign-extended or zero-extended (during bit-width inference).

The rule of thumb for both self-determined and context-determined expressions is that all its operands must be signed for the operator to be interpreted as signed (and therefore produce a signed output). There are the following exceptions:
* The result of concat is always unsigned
* The result of comparisons is always unsigned

Additionally, there are two conversion functions (`signed()`, `unsigned()`) which coerce results of partial expressions to be either signed or unsigned, respectively. Note that these functions **do not** affect the signedness of any operands of the partial expression being coerced, but do affect the signedness of any other expressions in which the partial expression appears. For example, in `x + signed(y + z)` the signedness of `y` and `z` is not affected, but `(y + z)` is interpreted as a signed value in the expression `x + (y + z)`.

### Summary of bit-width and signedness rules
| Expression             | Operands           | Output bit-width | Output signedness       |
|------------------------|--------------------|------------------|-------------------------|
| Binary arith.,logical  | Context-determined | max(operands)  | all(signed(operands)) |
| Unary logical          | Context-determined | max(operands)  | all(signed(operands)) |
| Shift                  | Shiftee context-determined, shifter self-determined, | Shiftee bit-width | all(signed(operands)) |
| Comparison             | Context-determined | 1                | unsigned                |
| Reduction              | Self-determined    | 1                | all(signed(operands)) |
| Concat                 | Self-determined    | sum(operands)  | unsigned |

## TODOs
* Integer operands
* Explicit extend operator
* SmartBits select operator
* Signedness for SmartBit
* Interoperability with existing non-smart code
* "Smart" blocks of code (e.g. avoiding writing smart every place)

## Further reading
* [Bit-width and signedness gotchas](http://www.deepchip.com/items/0466-05.html)

