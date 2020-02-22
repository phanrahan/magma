# New definition syntax
Magma provides an alternate (and preferred syntax) for defining circuits. This looks like

```
import magma as m

class Top(m.Circuit):
    io = m.IO(I0=m.In(m.Bit),
              I1=m.In(m.Bit),
              O=m.Out(m.Bits[2]))

    inner = InnerModule()
    m.wire(io.I0, inner.I)
    m.wire(inner.O, io.O[0])
    m.wire(io.I1, io.O[1])
```

This syntax differs from the original syntax in two main ways:
* `IO = ["name", type, ...]` -> `io = IO(name=type, ...)`
* The logic usually inside `def definition()` can now be inlined directly into the class-definition body. The ports normally accessibly through the attributes of the argument of this function can now be accessed as attributes of `io`.

Other than these minor changes (simplifications, really) to the definition syntax, the magma operates as before. In particular the syntax and semantics of wiring, instancing, and types *have not changed*.

# Notes
* This change updates the standard to make this new syntax preferred to the old syntax. Additionally, we are also deprecating the factory functions `DefineCircuit()` and `DeclareCircuit()`; these will continue to work but we suggest against using these methods.
* There maybe some robustness issues with the `isdefinition` introspection method. If you encounter these, please file issues.
