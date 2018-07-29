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
@m.circuit.combinational
def if_statement_basic(I: m.Bits(2), S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]

```

Basic nesting:
```python
class IfStatementNested(m.Circuit):
@m.circuit.combinational
def if_statement_nested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
    if S[0]:
        if S[1]:
            return I[0]
        else:
            return I[1]
    else:
        if S[1]:
            return I[2]
        else:
            return I[3]
```

Terneray expressions
```python
def ternary(I: m.Bits(2), S: m.Bit) -> m.Bit:
    return I[0] if S else I[1]
```

Nesting terneray expressions
```python
@m.circuit.combinational
def ternary_nested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
    return I[0] if S[0] else I[1] if S[1] else I[2]
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
