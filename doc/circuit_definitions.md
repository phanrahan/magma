# Combinational Circuit Definitions
Circuit defintions can be marked with the `@m.circuit.combinational` decorator.
This introduces a set of syntax level features for defining combinational magma
circuits, including the use of `if` statements to generate `Mux`es.

This feature is currently experimental, and therefor expect bugs to occur.
Please file any issues on the magma GitHub repository.

## If and Ternary
The condition must be an expression that evaluates to a `magma` value.

Basic example:
```python
class IfStatementBasic(m.Circuit):
    IO = ["I", m.In(m.Bits(2)), "S", m.In(m.Bit), "O", m.Out(m.Bit)]
     @m.circuit.combinational
    def definition(io):
        if io.S:
            O = io.I[0]
        else:
            O = io.I[1]
        m.wire(O, io.O)

```

Basic nesting:
```python
class IfStatementNested(m.Circuit):
    IO = ["I", m.In(m.Bits(4)), "S", m.In(m.Bits(2)), "O", m.Out(m.Bit)]
     @m.circuit.combinational
    def definition(io):
        if io.S[0]:
            if io.S[1]:
                O = io.I[0]
            else:
                O = io.I[1]
        else:
            if io.S[1]:
                O = io.I[2]
            else:
                O = io.I[3]
        m.wire(O, io.O)
```

Terneray expressions
```python
class Ternary(m.Circuit):
    IO = ["I", m.In(m.Bits(2)), "S", m.In(m.Bit), "O", m.Out(m.Bit)]
     @m.circuit.combinational
    def definition(io):
        m.wire(io.O, io.I[0] if io.S else io.I[1])
```

Nesting terneray expressions
```python
class TernaryNested(m.Circuit):
    IO = ["I", m.In(m.Bits(3)), "S", m.In(m.Bits(2)), "O", m.Out(m.Bit)]
     @m.circuit.combinational
    def definition(io):
        m.wire(io.O,
               io.I[0] if io.S[0] else io.I[1] if io.S[1] else io.I[2])
```

Things that aren't supported:
* Using anything other than an assignment statement in the if/else body
* Assigning to a variable only once in the if or else body (not both). We could
  support this if the variable is already defined in the enclosing scope, for
  example using a default value
    ```
    x = 3
    if S:
       x = 4
    ```
* This brings up another issue, which is that it doesn't support a default
  value. (So the above code would break even if x was assigned in the else
  block.
* If without an else (for the same reason as the above)
