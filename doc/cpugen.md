# Creating soft cores / state machines with CPUGEN

CPUGEN is a domain-specific language for creating state machines.
Some examples of state machines for which CPUGEN can be used:

- Microcontrollers
- Soft cores
- Memory interfaces
- High-level synthesis

CPUGEN is a compiler. It takes a program describing a state machine as input,
and generates an interface in Magma for interacting with the rest of the circuit.

## Usage

Set the environment variable `MAGMA_BIN` to the `bin` subdirectory of this repo,
and then add `MAGMA_BIN` to your `PATH`:

    export PATH=$MAGMA_BIN:$PATH

The CPUGEN-relevant binaries/scripts `cpugen[.exe], makecpu`, and `cpugen.py` will become available.

To synthesize a CPU, we first need to decide on the name, which will be used in the resulting Magma library.
Suppose the name is `basename`.

### Footer file

CPUGEN operates on `*.ss` files, turning them into Magma files (`.py`).
But first, in order to interface with the rest of Magma, the file `basename_footer.py`
must be available in the same directory as the `basename.ss` file.

See `test6/cpugen/pico1/pico1_footer.py` for an example.

#### synthesize_fsm

Every synthesized CPU will make available the `synthesize_fsm` procedure,
which takes the system clock `clk` and optional pulse `pulse` as arguments 
(in order to run machines slower than the clock for debugging).
It is up to you to define the interface and how `synthesize_fsm` is called.

### Compiling to Magma

After the footer is created, we can now use CPUGEN to compile the state transitions to a Magma circuit generator.
To do this, issue

    makecpu name/of/cpu/basename.ss

Indeed, the argument to makecpu can contain directories,
but it must end with `<name-of-cpu>.ss`.
CPUGEN will then generate `name/of/cpu/basename.py`.

# CPUGEN Concepts

## Single-cycle transition

The key concept needed to understand and write programs in CPUGEN is the "single-cycle transition,"
or what kinds of state changes may happen in a single cycle.
CPUGEN programs describe essentially, only the single-cycle transitions,
with the clock signal and external components being either implicit
or defined outside CPUGEN in Magma.

In Verilog and other hardware description languages, we might describe single-cycle transitions
by setting up an "always" block with a clock signal, 
and then describing state changes inside this block:

    rocket.v:
    
    reg [15:0] a;
    reg [15:0] b;
    reg phase;
    
    always@{posedge CLK}
    begin
       if phase == 0 begin
           if ((a % 16'd44) == 0) begin
               b <= b + 1;
           end
           a <= a + 1;
           ...<other state changes>...
           phase = 1;
       end
       if phase == 1 begin
           a <= a + 2;
           ...<other state changes>...
           phase = 0;
       end
    end

This can be confusing, because we do not always know what kinds of registers
may be inferred from this code.
Also, this sort of code does state changing, which can be confusing
when it mixes with other types of code that can have completely
different paradigms, like creating and wiring up components.

Finally, this is not depicted in the example above,
but in Verilog, one may mix non-blocking and blocking assignments,
which can cause confusion.

The equivalent CPUGEN program would look like this:

    rocket.ss:
    
    (define-register a 16)
    (define-register b 16)
    
    (define-transition phase0
        (if (= (mod a 44) 0)
          (set! b (+ b 1)))
        (set! a (+ a 1))
        ...<other state changes>...
        (set-next phase1))
    
    (define-transition phase1
        (set! a (+ a 2))
        ...<other state changes>...
        (set-next phase0))
 
CPUGEN programs define similar things versus that of always blocks, with a few important differences:

- The clock signal is implicit and left up to the surrounding Magma program.
- There is no mixing of _state-changing_ versus _wiring_ code, so the CPUGEN program with its register declarations constitute a well-defined state machine.
- Phases of the machine can be explicitly named through different `define-transition`'s.
- (Not pictured) Pipelines can also be defined using the `define-pipe` primitive.

## CPUGEN program format

The program input to CPUGEN takes the following form:

    [register declarations]
    [RAM declarations]
    [function: pipe | transition | helper]

See `test6/cpugen/pico1/pico1.ss` for an example where CPUGEN is used to define a Pico processor.
We will use this example throughout this section.

### Register declarations

Register (and RAM) declarations specify the extent of the state 
on which the transition functions will operate.
Register declarations specify the name and width (in bits) of the register.
For the Pico, it is sufficient to define registers for the stack pointer, IO port, and zero/carry flags:

    (define-register SP 8)
    (define-register IO 8)
    (define-register Z 1)
    (define-register C 1)

### RAM declarations

RAM declarations are similar, but with RAM-specific parameters.
The following RAM declarations define:

- A dual-port (`D`) register file, `AXBX`, with 1024 entries and each entry being 16 bits wide.
- A single-port (`S`) program memory, `PROG`, with 16 entries and each entry being 18 bits wide.
- A single-port (`S`) program memory, `STACK`, with 16 entries and each entry being 8 bits wide.

The actual declarations are as follows:

    (define-ram AXBX D 1024 16)
    (define-ram PROG S 16 18)
    (define-ram STACK S 16 8)

This defines the register file, program memory, and stack memory of the Pico processor.

### Defining transitions

Now we define transitions on the state (registers and RAMs) above. 
See `test6/cpugen/pico1/pico1.ss` for the details.
For the Pico processor, it is possible to fit instruction fetch, decode, and ALU execution 
in one clock cycle, so we will have one transition:

    (define-transition fetchdecode-alu
       ...)

This transition will involve some initial setup, such as finding the top of the stack using the
`SP` register:

    (set! (STACK ADDR) SP)

This is a `set!` statement. All state-changing transitions will use `set!`.
Here, we are setting the next value of the `ADDR` (address) port of the ram called `STACK`,
to the current value of the stack pointer (`SP`).

`set!` is not the only way to specify transitions. It is useful to have a concept of intermediate variable,
that does not need to be a register, but still carries useful information.
We use `let` to specify these values.  For example, the program counter, `PC`, is such an intermediate value,
derived from the output of the `STACK` RAM:

    (let PC (: STACK 0 8))

This statement defines a new intermediate value, `PC`, that is the first 8 bits of the output of the `STACK` RAM.

#### Blocking and non-blocking assignments    

`set!` statements are analogous to non-blocking assignments in Verilog;
any register appearing on the RHS refer to the value at the previous cycle,
and not the most recent value set, as would be the case with blocking assignments.

Conversely, intermediate values (with `let`) are defined in a blocking manner,
befitting their role as combinational wires inside a transition.

As `set!` is the only way to set the value of a register, there is 
no confusion between blocking/non-blocking ways to set registers,
(as is the case in Verilog).

#### Conditional transitions

It is difficult to define any sort of state machine without being able to define conditional transitions;
that is, transitions where a piece of state is set or not, depending on the value of something else.

In the Pico processor, one such place where conditional transitions are needed 
is in extracting the value of the operand, which can either be encoded in the instruction (immediate)
or the `B` port of the register file:

    (let BXV (cond notimmediateflag (: (AXBX B) 0 8) imm))

We see that `cond` works similarly to C's ternary operator; it is a pure function that is used to select between two potential values.

Of course, not every conditional transition is a pure function; 
sometimes, it can involve setting some state, or letting that state continue being 
its previous value. 
For these, we use `if` / `case`.

The following code selects between different state-changing operations,
depending on the value of `insttype` (representing the type of instruction):

    (if (= (bv 1 1) insttype)
        (do-jumpcall op AXV addr kaddr PC)
        (do
          (case insttype
            (0 0) (write-AX! BXV)
            (1 0) (do-arith op AXV BXV)
            (0 1) (set! IO BXV))
          ))

`if` statements are used to select between two different state changing actions.
When multiple alternatives need to be considered, `case` is used.
Both `if` and `case` work similarly to their Verilog counterparts.
