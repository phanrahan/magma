# Mantle

Mantle is a library of parameterized hardware primitives.
It provides functionality similar to the classic 
7400 series TTL and 
4000 seris CMOS integrated circuits.

## Combinational Logic

### Lookup Tables (LUTs)

The fundamental combinational primitive in an FPGA 
is a lookup-table, or LUT.
LUTs are indexed by an n-bit value.

The argument to the LUT function initializes the LUT. 
```init``` can be an int, a sequence, or an expression.

If ```init``` is a Sequence of 0s and 1s, 
each output bit in the table is initialized with those values.
An n-bit LUT is initialized with a sequence of length  2^n.
For example, to create a 2-input and gate,
```LUT2``` can be initialized to with the sequence```[0,0,0,1]```.

If ```init``` is an int, then the int is converted to a list of bits.
If the LUT contains n-bits, the sequence used to initialize is is 2^n bits.
The bit in the sequence, is set to the bit in ```init```.
For example, initializing ```LUT2``` with ```init=0x8``` 
is equivalent to initializing it to ```[0,0,0,1]```.
The 4th entry in the sequence is 1 because
the both bit in ```0x8``` is set.
All the other entries in the sequence are 0,
since all the other bits in ```init``` are cleared.
Since the number of bits depends on the size of the LUT,
using this method of initialization requires you to set
the size of the LUT by calling a LUT function with
a known numbers of bits 
(in this case, ```LUT2``` or ```LUTN(init,2)```;
you cannot call the general ```LUT``` function.

Integer expressions can also be created from python expressions.
The constants ```I0```, ```I1```, ```I2```, and ```I3``` 
have been predefined values.  
For example, ```LUT2(I0 & I1)``` will create an ```LUT```
which corresponds to a 2-input and gate.

The final way to initialize an ```LUT``` is to use a python function.
This function will be called for each input value,
and should return True or False.

The various LUT functions are shown below.
Note that we are using type signatures to indicate
the inputs and the outputs of the circuit.
For example, ```I0, I1 -> O``` 
indicates that there are two inputs named ```I0``` and ```I1```,
and a single outout ```O```.


```
lut = LUT1(init) :: I0:Bit -> O:Bit
lut = LUT2(init) :: I0:Bit, I1:Bit -> O:Bit
lut = LUT3(init) :: I0:Bit, I1:Bit, I2:Bit -> O:Bit
lut = LUT4(init) :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit
lut = LUT5(init) :: I0:Bit, I1:Bit, I2:Bit, ..., I4:Bit -> O:Bit
lut = LUT6(init) :: I0:Bit, I1:Bit, I2:Bit, ..., I5:Bit -> O:Bit
lut = LUT7(init) :: I0:Bit, I1:Bit, I2:Bit, ..., I6:Bit -> O:Bit
lut = LUT8(init) :: I0:Bit, I1:Bit, I2:Bit, ..., I7:Bit -> O:Bit

lut = LUTN(init, n) :: I0:Bit, ..., In:Bit -> O:Bit
lut = LUT(init) :: I0:Bit, ..., In:Bit -> O:Bit
```

### ROM

The ```ROM``` functions are very similar to the ```LUT``` functions.
The only difference is the the types of the inputs.
The ```LUT``` versions take n input arguments of type Bit.
The ```ROM``` versions of these functions take
a single input, an ```Array(n,Bit)```.

```
rom = ROM1(init) :: I:Array(1, Bit) -> O:Bit
rom = ROM2(init) :: I:Array(2, Bit) -> O:Bit
rom = ROM3(init) :: I:Array(3, Bit) -> O:Bit
rom = ROM4(init) :: I:Array(4, Bit) -> O:Bit
rom = ROM5(init) :: I:Array(5, Bit) -> O:Bit
rom = ROM6(init) :: I:Array(6, Bit) -> O:Bit
rom = ROM7(init) :: I:Array(7, Bit) -> O:Bit
rom = ROM8(init) :: I:Array(8, Bit) -> O:Bit

rom = ROMN(init, n) :: I:Array(n, Bit)  ->  O:Bit
rom = ROM(init) :: I:Array(n, Bit)  -> O:Bit
```

```
defrom = DefineROM16XN(rom) :: I:Array(16, Bit) -> O:Array(n, Bit)
rom = ROM16XN(rom) :: I:Array(16, Bit) -> O:Array(n, Bit)
```

### MUXs

The second fundamental combinational primitive 
in an FPGA is a multiplexer, or a MUX.

The simplest MUXes select amongts a small number of inputs.
```I``` is an array of n bit values, or ```Array(n,Bit)```
```S``` is the selector; it has ```log(n)``` bits.

```
mux = Mux2() :: I:Array(2, Bit), S:Bit -> O:Bit
mux = Mux4() :: I:Array(4, Bit), S:Array(2, Bit) -> O:Bit
mux = Mux8() :: I:Array(8, Bit), S:Array(3, Bit) -> O:Bit
mux = Mux16() :: I:Array(16, Bit), S:Array(4, Bit) -> O:Bit
```

```
mux = MuxN(n={2,4,8,16}) :: I:Array(n, Bit), S:Array(log(n), Bit) -> O:Bit
```

A more general MUX selects amongst ```height``` inputs
each with a given ```width```.

```
mux = Mux(height, width) :: 
    I:Array(height, Array(width, Bit)),
    S:Array(log(height), Bit) 
    -> O:Array(height, Bit)
```


### Logic
```
op = And2() :: I0:Bit, I1:Bit -> O:Bit
op = And3() :: I0:Bit, I1:Bit, I2:Bit -> O:Bit
op = And4() :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit

op = NAnd2() :: I0:Bit, I1:Bit -> O:Bit
op = NAnd3() :: I0:Bit, I1:Bit, I2:Bit -> O:Bit
op = NAnd4() :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit

op = Or2() :: I0:Bit, I1:Bit -> O:Bit
op = Or3() :: I0:Bit, I1:Bit, I2:Bit -> O:Bit
op = Or4() :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit

op = NOr2() :: I0:Bit, I1:Bit -> O:Bit
op = NOr3() :: I0:Bit, I1:Bit, I2:Bit -> O:Bit
op = NOr4() :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit

op = Xor2() :: I0:Bit, I1:Bit -> O:Bit
op = Xor3() :: I0:Bit, I1:Bit, I2:Bit -> O:Bit
op = Xor4() :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit

op = NXor2() :: I0:Bit, I1:Bit -> O:Bit
op = NXor3() :: I0:Bit, I1:Bit, I2:Bit -> O:Bit
op = NXor4() :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit
```

The following functions are wide versions of the basic logic functions.
The number of inputs is equal to the height ```h```.
Each input and output are arrays of width ```w``` bits.
```
op = And(h, w)  :: I0:Array(w,Bit), ..., Ih:Array(w,Bit) -> O:Array(w,Bit)
op = NAnd(h, w) :: I0:Array(w,Bit), ..., Ih:Array(w,Bit) -> O:Array(w,Bit)
op = Or(h, w)   :: I0:Array(w,Bit), ..., Ih:Array(w,Bit) -> O:Array(w,Bit)
op = NOr(h, w)  :: I0:Array(w,Bit), ..., Ih:Array(w,Bit) -> O:Array(w,Bit)
op = Xor(h, w)  :: I0:Array(w,Bit), ..., Ih:Array(w,Bit) -> O:Array(w,Bit)
op = NXor(h, w) :: I0:Array(w,Bit), ..., Ih:Array(w,Bit) -> O:Array(w,Bit)
```

The following functions compute a logical function
of an array of ```n``` Bits.
```
op = AndN(n)  :: I:Array(n:Bit) -> O:Bit
op = NAndN(n) :: I:Array(n:Bit) -> O:Bit
op = OrN(n)   :: I:Array(n:Bit) -> O:Bit
op = NOrN(n)  :: I:Array(n:Bit) -> O:Bit
op = XorN(n={1,2,3,4})  :: I:Array(n:Bit) -> O:Bit
op = NXorN(n={1,2,3,4}) :: I:Array(n:Bit) -> O:Bit
```

Form the logical negation of a single bit.
```
op = Not() :: I:Bit - O:Bit
```

Invert an ```n``` bit array.
```
op = Invert(n) :: I:Array(n,Bit) - O:Array(n,Bit)
```


### Comparison

These functions implement comparison tests between to n-bit inputs.

Equality and inequality testing.

```
op = EQ(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
op = NE(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
```

Signed comparisons.
```
op = LT(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
op = LE(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
op = GT(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
op = GE(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
```

Unsigned comparisons.
```
op = ULT(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
op = ULE(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
op = UGT(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
op = UGE(n) :: I0:Array(n,Bit), I1:Array(n,Bit) -> O:Bit
```

### Decoders, Encoders, and Arbiters

Mantle has a decoders, encoders, and arbiters.

```
Decode
```

returns circuit that computes whether the n-bit input is equal to i.

```
op = Decode(i,n) :: I:Array(n,Bit) -> O:Bit
```
For example, ```Decode(3,4)``` returns whether the 4-bit input is
is equal to 3.

```
Decoder
``` 

maps from single input to multiple outouts.
Decoder accepts a single n-bit input,
and returns 2^n single bit outputs.
The ith output is 1, if the input is equal to i.
```
op = Decoder(n) :: I:Array(n,Bit) -> O:Array(2^n,Bit)
```
For example, 
`Decoder(3) :: I:Array(3,Bit) -> O:Array(8,Bit)` sets `O[i] = (i == I)`.


An encoder is the inverse of a decoder.
An encode accepts a single 2^n-bit input,
and outputs the n-bit binary value representing that input..
```
op = Encoder(n) :: I:Array(n,Bit) -> O:Array(log(n),Bit)
```
Since the number of output bits is less than the number of input bits,
multiple input values will map to the same output.
Normally encoders are designed such that an input
will only a single bit set, 
will yield the log(n) bit representation of the position of the bit.
If multiple bits are set,
the log(n) bit representations for each set bit are or'ed together.


An arbiter or priority encoder is an special encoder.
The output is set to the encoder value of the least significant set bit.
If other bits are set, the output does not change.
```
op = Arbiter(n) :: I:Array(n,Bit) -> O:Array(log(n),Bit)
```


### Arithmetic
```
add = Add(n, cin=0)
adc = AddC(n, cin=0)

sub = Sub(n, cin=1)
sbc = SubC(n, cin=1)
```

```
neg = Negate(n)
```

```
# NYI
mul = Mul(n, m)
```


## Sequential Logic

### Flip-Flops
```
# DFF :: I:Bit -> O:Bit
DFF(init=0, ce=False, r=False, s=False)
```

```
# SRFF :: S:Bit, R:Bit -> O:Bit
SRFF(init=0, ce=False)
```

```
# RSFF :: R:Bit, S:Bit -> O:Bit
RSFF(init=0, ce=False)
```

```
# JKFF :: J:Bit, K:Bit -> O:Bit
JKFF(init=0, ce=False, r=False, s=False)
```

```
# TFF :: I:Bit -> O:Bit
TFF(init=0, ce=False, r=False, s=False)
```
If I is true, toggle the flip-flop.

There is also a utility function to create a list of n ```DFF```s

```
FFs(n, init=0, ce=False, r=False, s=False)
```


### Registers
```
# Register :: I:Array(n,Bit) -> O:Array(n,Bit)
Register(n, init=0, ce=False, r=False, s=False)
```

### Shift Registers
```
# SIPO :: I:Bit -> O:Array(n, Bit) 
SIPO(n, init=1, ce=False, r=False, s=False)

# SIPO :: I:Bit -> O:Bit
SISO(n, init=1, ce=False, r=False, s=False)

# SIPO :: SI:Bit, PI:Array(n, Bit), LOAD:Bit  -> O:Bit
PIPO(n, init=1, ce=False, r=False, s=False)

# PIPO :: SI:Bit, PI:Array(n, Bit), LOAD:Bit  -> O:Array(n, Bit)
PISO:Bit(n, init=1, ce=False, r=False, s=False)
```

```
# Ring :: None -> O:Array(n,Bit)
Ring(n, init=1, ce=False, r=False, s=False)
```

```
# Johnson :: None -> O:Array(n,Bit)
Johnson(n, init=1, ce=False, r=False, s=False)
```

```
# CascadedRing :: CE:Bit -> O:Bit
CascadedRing(n, init=1, ce=False, r=False, s=False)
```

### Counters

Counters have a ```COUT```.
```
# Counter :: None -> O:Bit:Array[n, Bit], COUT:Bit
Counter(n, next=False, ce=False, r=False, s=False)
```
Create an n-bit counter, with optional `CE` (clock enable), `RESET`, and `SET`.

The counter consists of an adder connected to a register.
The adder is combinational and is computing the next value
of the counter by incrementing the current value.
Normally the output of the counter is the register,
but by setting `next=True`, the output is the adder.

The adder also generates a carry, `COUT`.
`COUT` will be true if the current value is generating a carry.
For example, an 8-bit counter will generate a COUT 
when the count equals 255.

```
# UpDownCounter :: Up:Bit, Down  Bit -> O:Array[n, Bit], COUT:Bit
UpDownCounter(n, next=False, ce=False, r=False, s=False)
```
Generate an up-down counter.
The counter is incremented by (Up-Down).

```
counter = CounterModN(m, n)
```
Counter clears when count equals m-1.

```
counter = CounterIncr(n)
```

## RAMs 

### RAM16

```
# RAM16x1 :: A:Array4, I:Bit, WE:Bit -> O:Bit
ram = RAM16X1(ram)

# RAM16x2 :: A:Array4, I0:Bit:Bit, I1:Bit:Bit, WE:Bit -> O:Bit0:Bit, O:Bit1:Bit
ram = RAM16x2(ram)

# NYI
# RAM16xN :: A:Array4, I:Array(n,Bit), WE:Bit -> O:Bit:Array(n,Bit)
ram = RAM16xN(ram)
```

```
# RAM16Dx1 :: A0:Array4, A1:Array4, I:Bit, WE:Bit -> O:Bit0:Bit, O:Bit1:Bit
ram = RAM16Dx1(ram)

#
# RAMN6Dx1 :: A0:Array4, A1:Array4, I:Bit, WE:Bit 
#              -> O:Bit0:Array(n,Bit), O:Bit1:Array(n,Bit)
ram = RAM16DxN(ram)
```

```
# NYI 
# RAM32x1 :: A:Array5, I:Bit, WE:Bit -> O:Bit
RAM32x1(ram)
```

### Blocked RAM

```
# ROMB :: A:Array(height,Bit) -> O:Bit:Array(width,Bit)
rom = ROMB( rom, width, init=None )
```

```
# NYI
ram = RAMB( ram, width, init=None )
```

