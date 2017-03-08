# Lattice ICE40

These functions are specific to the Lattice ICE40 Devices.

## Combinational Lofic

### LUTS

```
SB_LUT4() :: I0:Bit, I1:Bit, I2:Bit, I3:Bit -> O:Bit
```

The LUT is initialized by setting the parameter INIT.

### Carry 

```
SB_CARRY() :: I0:Bit, I1:Bit, CI:Bit -> CO:Bit
```

This functional unit computes the carry out give
3 inputs, including the carry in from the previous logic cell.

```
CO = (I0&I1)|(I1&CI)|(CI&I0)
```

### Flip-Flops

```
SB_DFF() :: C:bit, D:Bit -> Q:Bit
```

```
# DFF w/ Clock enable
SB_DFFE() :: C:bit, E:Bit, D:Bit -> Q:Bit
# DFF w/ Synchronous Reset
SB_DFFSR() :: C:bit, R:Bit, D:Bit -> Q:Bit
# DFF w/ Asynchronous Reset
SB_DFFR() :: C:bit, R:Bit, D:Bit -> Q:Bit
# DFF w/ Synchronous Set
SB_DFFSS() :: C:bit, S:Bit, D:Bit -> Q:Bit
# DFF w/ Asynchronous Set
SB_DFFS() :: C:bit, S:Bit, D:Bit -> Q:Bit
# DFF w/ Synchronous Reset, Clock enable
SB_DFFESR() :: C:bit, E:Bit, R:Bit, D:Bit -> Q:Bit
# DFF w/ Asynchronous Reset, Clock enable
SB_DFFER() :: C:bit, E:Bit, R:Bit, D:Bit -> Q:Bit
# DFF w/ Synchronous Set, Clock enable
SB_DFFESS() :: C:bit, E:Bit, S:Bit, D:Bit -> Q:Bit
# DFF w/ Asynchronous Set, Clock enable
SB_DFFES() :: C:bit, E:Bit, S:Bit, D:Bit -> Q:Bit
```

### Blocked RAM
```
ram = SB_RAM40_4K() ::
    RADDR:Array(11,Bit),
    RCLK:Bit,
    RCLKE:Bit,
    RE:Bit,
    WCLK:Bit,
    WCLKE:Bit,
    WE:Bit,
    WADDR:Array(11,Bit),
    MASK:Array(16,Bit),
    WDATA:Array(16,Bit)
    -> 
    RDATA:Array(16,Bit)
```

### IO

```
SB_IO() ::
    CLOCK_ENABLE:Bit,
    INPUT_CLOCK':Bit,
    OUTPUT_CLOCK':Bit,
    OUTPUT_ENABLE':Bit,
    LATCH_INPUT_VALUE':Bit,
    D_IN_0':Bit, # rising
    D_IN_1':Bit, # falling
    PACKAGE_PIN: Bit # inout
    ->
    D_OUT_0':Bit, # rising
    D_OUT_1':Bit, # falling
    PACKAGE_PIN: Bit # inout
```

This primitive is controlled using the parameter `PIN_TYPE`.
