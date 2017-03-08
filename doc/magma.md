## Magma Programming Model

Magma is a Low-Level Hardware Design Language (LLHDL) for FPGAs.
In contrast, verilog and VHDL are high-level hardware design languages.

Think of Magma as a hardware assembly language.
Programming in Magma is like writing programs in assembly language.
This is useful if you want total control of the hardware,
but it is low-level and should only be done when necessary.

Magma is inspired by LLVM, a low-level virtual machine IR
that is used to compile high-level languages to different processors.
Magma is designed as a target for a compiler
that converts a higher-level language into lower-level hardware.
This is particularly easy to do,
since Magma is embedded in python,
a nice programming language 
for building higher-level libraries and domain-specific languages.
Magma is essentially a Register Transfer Language (RTL),
a low-level intermediate representation 
used by compiler writers and hardware designers.


#### Creating Hardware Primitives

The first step in using Magma is to configure the FPGA hardware primitives.
The three most common primitives in FPGAs are lookup tables (LUTs),
D-flip-flops (FFs), and input/output buffers (IOBs).

For example, the following code snippet
```
logic1 = LUT2(I0&I1)
logic2 = LUT2(I0|I1)
```
will create 2 lookup tables,
each with 2 inputs and 1 output.
Each input and output is 1 bit.
Printing `logic1`
```
print logic1
I0, I1 -> O
```
shows that `logic1` is a function that maps from two bits to one bit.

`LUT` is a python function 
that allocates and configures a hardware lookup table.
Each invocation of `LUT` allocates and configures a new lookup table.
The value returned by `LUT` and assigned to `logic1`
refers to the hardware lookup table.
The hardware lookup table is a function,
because it maps from its inputs to an output,
However, `logic1` is not a normal python function.
A python function runs immediately on the host computer.
The hardware functional unit implemented in the lookup table
runs on the FPGA after it is loaded into the FPGA.
When writing Magma programs, it is important to 
keep in mind whether a function is a python function
or a hardware functional unit.

The contents of the lookup table 
are set to correspond to the given logical expresson.
To implement the 2 bit and function,
the table is initialized to `[0,0,0,1]`.

When configuring lookup tables using string expressions,
the order of the arguments to the functional unit 
is the same as the alphabetical order of the variables used.
In these examples, the sorted order of the variables is `A` then `B`,
so the first input to logic1 will be `A` and the second input will be `B`.
Of course, in these examples the order doesn't matter
because `A&B=B&A` and `A|B=B|A`.

Another common hardware primitive is a D flip-flop,
```
ff = FF()
```

The final common hardware primitive are the
IO buffers that are connected to pins.
```
switch1 = In(90)
switch2 = In(91)

led1 = Out(94)
led2 = Out(95)
```
This program configures pins 90 and 91 for input,
and 94 and 95 for output.
Input and output pins are special cases of hardware functions.
The input to the input pin is off-chip, the output is a bit.
Conversely, the input to an output pin is a bit,
and the output goes off-chip.
In this hypothetical example,
the input pins are connected to manual switches 
and the output pins are connected to LEDs.

In hardware, bits are represented as voltages.
Magma defines
```
GND
VCC
```
to indicate ground and power.
Since in python we normally represent bits
as boolean values (False or True, 0 or 1),
Magma considers 0 to be equivalent `GND`,
and 1 to be equavalent to `VCC`.


#### Wiring Functional Units

The next step is to wire functional units together to create a circuit.
This involves connecting the output of one functional unit 
to the input of another function unit.

Magma uses function call syntax for wiring.
```
f = logic1( switch1, switch2 )
led1( f )
```
Calling `logic1` with two arguments,
will wire the arguments to the inputs of the function.
In this example, 
the first statement wires `switch1` and `switch2` 
to the input 0 and input 1  of the logic1 function,
and the second statement wires the output of the `logic1` function 
to input of the `led1` function.
This will cause the LED to display the logical and of the two switches.

We can easily superimpose a `FF` in that circuit.
```
f = ff ( logic1( switch1, switch2 ) )
led1( f )
```
This can be shortened to
```
led1( ff ( logic1( switch1, switch2 ) ) )
```

An equivalent way to wire up functional units is to use the `wire` function.
```
f = ff ( logic1( switch0, switch1 ) )
wire( f, led )
```
The general form of the `wire` function is
```
wire( O, I )
```
which wires the outputs of the first argument
to the inputs of the second argument.

Finally, a warning.
Assignment is not equivalent to wiring.
```
led1 = logic1( switch1, switch2 )
```
does not wire the output of `logic1` to `led1`. 
It assigns the output of `logic1` to the python variable `led1`.

#### Creating New Functions 

A `LUT` can be used configured
to precompute any logical function of its inputs.
```
logic3 = LUT3((~I2 & I0) | (I2 & I1))
```
will create a logical function of three values.
The function signature is
```
print logic3
[3] -> 1
```
The output of this function will be `I2 ? I1 : I0`.

All programming models need some way 
to abstract common programming operations into new functions.
Suppose we want to create new function `Mux2` that is
implemented using `logic3`.
```
mux2 = Mux2()

wire( mux2( array(switch0, switch1), switch2 ), led1 )
```
The first argument to `Mux2` would be an array of two inputs,
the second argument would be a selector. 

Here is the implementation of `Mux2`.
```
def Mux2():

    A = Bit()
    B = Bit()
    C = Bit()

    mux = LUT3((~I2 & I0) | (I2 & I1))

    O = mux( A, B, C )

    I = array(A, B)
    S = C

    return Circuit("input I", I, "output O", O )
```
First, we create three named arguments, `A`, `B`, `C`, to the new function.
Second, we create the the body of the function.
In this case the `mux` function using a `LUT`.
Then we wire up the arguments to `mux`.
The output of `mux` is returned as `O`.
The final step is to create a new function using `Function`.
The first argument to `Function` is the inputs.
In this example, there are two input arguments `I` and `S`.
The second argument is the output of the function.
We can see this by printing out the function signature
```
print Mux2()
[[2], 1] -> 1
```


#### More Powerful Wiring Functions

The function `wire` is a function that wires the
output of one function to the input of another function.
`wire` itself is a python function that takes magma functions as arguments.
In functional programming, the term higher-order function is used
to indicate a function which takes functions are arguments.
Thus, `wire` is a higher-order function.

Another way to think of wiring is as function composition.
If you have two functions f(x) and g(x) where the outputs
of g match the inputs of f,
we can compose f with g to create a new function h.
f composed with g equals f(g(x)).
This is equivalent to `wire(g, f)`.

Function composition in Magma is completed supported.
```
h = compose( f, g )
```
which is also implemented with the power (`**`) operator.
```
h = f ** g
```
This creates a new function `h` whose inputs are the inputs of `g`,
and whose outputs are outputs of `f`.

We can wire the switches directly to the leds succinctly with
```
led1 ** switch1
led2 ** switch2
```

An even more powerful way to combine functions into circuits 
is to use `fork` and `join`.
Consider the program
```
leds = join( led1, led2 )
logics = fork( logic1, logic2 )

leds( logics( switch1, switch 2 )
```
The arguments to `join` are two functions;
`join` forms a new function by concatenating the inputs and the outputs
of the functions being joined.
In this case, `led0` and `led1` each have one input and one output.
Joining them together creates a new function `leds`
that has two inputs and two outputs.
The first input of the combined function is connected to `led1`,
and the second input is connected to `led2`.

![alt tag](images/join.png)

`fork` is a bit different.
`logic1` and `logic2` each take two inputs and have one output.
Forking them together creates a new function `logics` 
which still has two inputs, and two outputs.
The first input of the new function
is wired to the first input of both `logic1` and `logic2`,
and the secound input is wired to both second inputs.
The two outputs are unioned together.
If we call `logics` with two inputs,
we wire up the inputs to both functions.

![alt tag](images/fork.png)

The program above wires the two switches to the two logic functions,
and then wires the two outputs to the leds.
Pretty cool!


#### Placing Multiple Functional Units

FPGAs consist of a 2D array of slices at different (x, y) locations. 
Each slice consists of a small number of elements.
An element in turns consists of a LUT and a FF.
In the spartan3 family, each slice has two elements
and each LUT has four inputs;
in the spartan6 family, the slices have four elements,
and each LUT has 6-inputs.

An LUT or a FF can be placed at a particular location.
```
lut = LUT2(I0&I1)
```

A very common operation is to replicate n functional
units to make a larger functional unit.
For example, n FFs can be combined to make a register.
```
def Register(n, init):
    def ff(y):
        return FF(init[y])
    return join( col( ff, n ) )

N = 8
reg1 = Register(N, N/2*[1,0] )
reg2 = Register(N, N/2*[0,1] )
```
The function `ff` creates a single `FF`.
The `col` (column) function calls `ff` n times.
Each FF is placed in a column starting at the current position.
The `y` argument to `ff` indicate the relative position
of the FF in the column. This value is passed so that you can
initialize the FF differently depending on its position.
In this case, we use `y` to index the init array containing
different initial values for the FF.
The final `join` combines the n FFs into a single n bit register.

It is also possible to arrange functional units in a row. or a 2D block.
```
col(func, n)
row(func, n)
```
Or a 2D block.
```
tile(func, (nx, ny), (dx, dy))
```
The `tile` function calls `func` `nx` times `ny` times at
different `x` and `y` locations.
This function also has strides `dx` and `dy`. 
`x` is incremented by `dx`, 
and `y` by `dy`,
between invocatons of `func`.

#### Clocks and Sequential Circuits

Values are stored in flip-flops during the rising edge of a clock.

Flip-flops also have a clock enable (CE),
a reset (R), and a set (S).

Combinational logic is a DAG.

Sequential logic will have cycles.  
Break the cycle by declaring functions with state first.
Can wire these up as a DAG, including setting the next state.
