# Passes

Magma provides a standard library of passes.

## InsertPrefix
This pass inserts a prefix (e.g. "soc_") before the names of every circuit in a
design.  This is useful for integrating magma generated verilog with a larger
design where name collisions could occur.

To use the pass, simply instantiate the `InsertPrefix` class with the top level
circuit and the desired prefix and invoke the `run` method, for example:
```
from magma.passes import InsertPrefix

InsertPrefix(Main, "baz_").run()
```
