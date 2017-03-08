# Gettting Started with Magma and Mantle

Magma programs are written in python. 
There are two aspects to designing hardware using Magma.
First, functional units are created in hardware.
Second, the functional units are wired up to create circuits.
We create the circuit in Magma,
then download it to the FPGA.

Here is a basic Magma program that blinks an LED once per second.
```
from magma.shield.LogicStart import *

counter = Counter( 32 )

count = counter( 1 )

wire( count[24], LED[0] )
```
The first line in the program imports the library
needed to use the LogicStart Megawing shield 
that attaches to the Papilio One board.
If you are using another board or shield,
you would need to import the appropriate library.

The Mantle library is included with the import statement.
Mantle is a library of useful hardware primitives.
Mantle is to Magma, as the C standard library (stdlib) is to C.

One useful hardware primitive is a counter.
The second line in the program calls Counter with 32..
The call to Counter creates a -32 bit counter,
and returns that counter.
The counter is a hardware functional unit that will run on the FPGA.

The counter requires one input.
If that input is 1, the counter will increment by 1.
If it is 0, the counter would not increment.
By calling counter with an argument equal to 1,
we are wiring a constant high value to the input.
This will cause the counter to continuously to count.

Note the difference between hardware and software.
Hardware functions are always running,
whereas software functions only run when you call them.
When you call a hardware function, you wire up its inputs.

When the counter hardware primitive is called, it returns its output. 
In this case, the output is the current value of the counter.
Since, we created a 32 bit counter, the output will be a 32 bit value.
The output of the counter are wires connected to its current value.
Thus, the output is always current. 

The final line in the program wires bit 24 of the counter to LED[0].
This will cause the left-most LED on the LogicStart to flash at 1Hz.

There are a few additional things to note here.
First, all values on wires are bits,
which have only two values 0 or 1 (False or True).
Second, arrays of bits are just python lists.
```count[24]``` is bit 24 of the current count.

Why do we use bit 24 of count?
We want bit-24 to change at 1 Hz.
The Papilio board contains a clock connected to the counter.
Everytime the clock signal rises, the counter is incremented.
By default, the clock runs at 32 MHz, or 32-million times per second.
If we were to attach the clock directly to the LED,
it will flash on and off 32 million times per second,
which to us would look to us 
as if it was continuously on at half its maximum brightness.
We slow down the rate using the counter. If you do the math,
2^24 is 32 Mhz. So, bit 24 will only change once per second.

This simple program summarizes the key ideas in Magma.

First, we use python to create hardware. 
Hardware is like software in many ways,
but also different in important ways.
Hardware, like software, consists of functions.
The functions in hardware are logic gates organized into 
functional units that are continuously computing.

Magma uses the same function call notation for wiring.
The input arguments to the call are the inputs to the functional unit,
and the return value is the output of the functional unit.

In software, we issue sequences of function calls to create programs.
In hardware, we wire up functions to create circuits.
The circuits, like the functional units, are continuously computing.

We can think of hardware like software,
but we need to remember these differences.

Finally, we call this process meta-programming.
Meta-programming means that we write a program that creates another program.
In this case we write a program in python that
creates a program (circuit) that runs on the hardware.
When a software program runs, it is loaded into memory and then run.
Similarly, the circuit is downloaded to the FPGA and run.

