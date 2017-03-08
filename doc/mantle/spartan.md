# Spartan

These primitives are specific to the Spartan3 and Spartan6.

## Combinational Lofic

### LUTS

The Spartan6 has
```
rom = LUT5x2(rom1, rom2)
rom = LUT6x2(rom1, rom2)
```

## Memory

### Slice Memory
```
ram = RAM16(ram) 
ram = RAM16D(ram) 
ram = RAM16x2(ram) 
```

The following primitives are only available on the Spartan6. 

```
ram = RAM32(ram) 
ram = RAM32D(ram) 
ram = RAM32x2(ram) 
ram = RAM32Q(ram) 
```

```
ram = RAM64(ram) 
ram = RAM64D(ram) 
ram = RAM64Q(ram) 
```

```
ram = RAM128(ram) 
ram = RAM128D(ram) 
```

```
ram = RAM256(ram) 
```


### Blocked RAM
```
ram = RAMB16(ram, width)
ram = RAMB16D(ram, width) # dual-ported
```

### SRL
```
srl = SRL16(init=0)
srl = SRL32(init=0)
```

## Buffers

### Global Buffers
```
bufg = BufG()
bufg = BufGCE()
```

## Digital Clock Manager / PLL

### DCM
```
d = DCM(freq)
```

## IO

```
d = IOB(**params)
```
