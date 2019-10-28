**NOTE** This is a work in progress, please let us know via issue/gitter/email
if you'd like to see anything added to this.

This is inspired by https://github.com/freechipsproject/chisel-cheatsheet and
will be rendered in a similar single page layout soon.

# Basic Magma Constructs
Magma Values
```
class Test(Circuit):
    IO = ["I", In(Bits[5]), "O", Out(Bits[5])]

    @classmethod
    def definition(io):
        # Allocate `x` as a value of type `Bits`
        x = Bits[5]()
        # Wire io.I to x
        x <= io.I
        # Wire x to io.O
        io.O <= x
```

**NOTE** Currently magma only supports wiring two intermediate temporary values
if the driver already has a driver.  The following example will work, because `y` is 
driven by `io.I` before wiring to the temporary `x`.

```python
class Test(Circuit):
    IO = ["I", In(Bits[5]), "O", Out(Bits[5])]

    @classmethod
    def definition(io):
        x = Bits[5]()
        y = Bits[5]()
        y <= io.I
        x <= y
        io.O <= x
```
while this example will not work, because `y` has no driver when being wired to
`x`.  A fix for this issue is forthcoming.
```python
class Test(Circuit):
    IO = ["I", In(Bits[5]), "O", Out(Bits[5])]

    @classmethod
    def definition(io):
        x = Bits[5]()
        y = Bits[5]()
        y <= io.I
        x <= y
        io.O <= x
```
