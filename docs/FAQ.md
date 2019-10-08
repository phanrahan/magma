# join vs array
## Question
I tried to instantiate an array of `mantle.CounterLoad` as follows.

```python
iter_num = m.array(
    [mantle.CounterLoad(cntr_width, cin=False, cout=False, incr=1, has_ce=True,
                        has_reset=True, name=f"iter_num_{i}") 
     for i in range(num_cntrs)]
)
```

I got the following error.

```
ValueError: All fields in a Array or a Tuple must be the same typegot CounterLoad5CER(DATA: In(UInt[5]), LOAD: In(Bit), O: Out(UInt[5]), CLK: In(Clock), CE: In(Enable), RESET: In(Reset)) expected CounterLoad5CER(DATA: In(UInt[5]), LOAD: In(Bit), O: Out(UInt[5]), CLK: In(Clock), CE: In(Enable), RESET: In(Reset))
```

## Answer
`m.array` is used to convert magma types, so one can take a list of `m.Bit`s
and convert them into an `m.Array` type.  In this case, you're trying to convert
a list of instances and "join" there interfaces into an array. For this pattern,
use magma's `m.join` higher order circuit operator:
```
iter_num = m.join(
    [mantle.CounterLoad(cntr_width, cin=False, cout=False, incr=1, has_ce=True,
                        has_reset=True, name=f"iter_num_{i}") 
     for i in range(num_cntrs)]
)
```
See
https://github.com/phanrahan/magma/blob/master/docs/higher_order_circuits.md#join-flat-and-fork
for more information.
