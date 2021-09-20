**NOTE** This is an experimental feature, you will likely encounter bugs.
Please use GitHub Issues to report any problems or to provide us with feedback
on how to improve the syntax.

# Overview
The goal of the `m.inline_combinational` syntax is to improve the ergonomics of
using the `m.combinational` syntax described [here](./circuit_definitions.md).

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
instance) and it's ports to perform logic and wiring.
Notice that the code wires the `reg.I` using the `@=` operator inside the if
statement.  The `combinational` rewrite logic will change these statements to
assign to a temporary value, which will then get process by the SSA pass to
produce the final value (output of a mux or chain of muxes) which is then wired
to the original target (`reg.I` in this case).

# Internal Details
For more details on the rewrites, here are two dumps of the intermediate code
during the `inline_combinational` rewrite process:
1. Introduce temporary values.  At this point, the wiring targets (LHS of `@=`
   operators) are replaced with a temporary values
   (using the prefix `auto_prefix0`, so `auto_prefix00` is the first temporary,
   `auto_prefix01` is the second temporary, the 2nd digit is used for the
   unique id). These temporary values are returned from the function.
   ```python
   @m.inline_combinational(debug=True, file_name='inline_comb.py')
   def logic():
       if io.invert:
           _auto_prefix_00 = ~reg.O
           _auto_prefix_01 = ~reg.O
       else:
           _auto_prefix_00 = reg.O
           _auto_prefix_01 = reg.O
       return _auto_prefix_00, _auto_prefix_01
   ```
2. Run the standard combinational passes.  This removes the if statements by
   transforming them into muxes using SSA.  Notice the temporaries have an
   extra digit attached, which is a unique identifier introduced by SSA.
   ```python
   @m.inline_combinational(debug=True, file_name='inline_comb.py')
   def logic():
       _auto_prefix_000 = ~reg.O
       _auto_prefix_010 = ~reg.O
       _auto_prefix_001 = reg.O
       _auto_prefix_011 = reg.O
       _auto_prefix_002 = __phi(io.invert, _auto_prefix_000, _auto_prefix_001)
       _auto_prefix_012 = __phi(io.invert, _auto_prefix_010, _auto_prefix_011)
       __return_value0 = _auto_prefix_002, _auto_prefix_012
       return __return_value0
   ```

After this rewrite process, the `inline_combinational` logic calls the function
to produce the return value.  The function execution uses the enclosing scope
(so references like `reg.O` should behave as expected).  The return values are
wired to their target (e.g. `reg.I @= _auto_prefix_002`).
