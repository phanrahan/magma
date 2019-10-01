Examples of translating Verilog code to magma

# Counter with reset and enable 
## Verilog
```verilog
logic read;
logic [9:0] rd_ptr;

always_ff @(posedge clk, negedge rst_n) begin
    if(!rst_n) begin
        rd_ptr <= '0;
    end
    else if(read) begin
        rd_ptr <= rd_ptr + 1;
    end
end
```

## Base magma
```python
# Declare anonymous bit (like a wire)
read = m.Bit()

# Generate/Instance register
rd_ptr = mantle.Register(10, has_async_reset=True, has_ce=True, init=0)

# Wire read to clock enable
rd_ptr.CE <= read

# Increment logic
rd_ptr.I <= m.uint(rd.ptr.O) + 1
```

## Sequential Syntax
(treating `read` as an input)

```python
@m.circuit.sequential(async_reset=True)
class Circuit:
    def __init__(self):
        self.rd_ptr: m.Bits[10] = m.bits(0, 10)

    def __call__(self, read: m.Bit) -> m.Bits[10]:
        orig_rd_ptr = self.rd_ptr

        # FIXME: Bug in magma sequential means we always have to specify a next
        # value (won't use current value by default)
        self.rd_ptr = orig_rd_ptr

        if read:
            self.rd_ptr = m.uint(self.rd_ptr) + 1
        return orig_rd_ptr
```

# Array of registers

## Verilog
```verilog
logic [1023:0][15:0] register_array
```

## Base magma
```python
register_array = m.join([mantle.Register(1024) for _ in range(15)])
```

## Sequential Syntax
```python
@m.circuit.sequential
class Circuit:
    def __init__(self):
        self.register_array: m.Array[15, m.Bits[1024]] = \
            m.array([m.bits(0, 1024) for _ in range(15)])
```
