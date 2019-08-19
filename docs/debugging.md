# Debugging magma

"How do I get all the debug information in the coreir json?"

Two functions need to be called with the argument `True`: 
* `m.config.set_debug_mode`
* `m.set_codegen_debug_info`

Here's a code example:

```python
# main.py
import magma as m

m.config.set_debug_mode(True)
m.set_codegen_debug_info(True)
And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                        "O", m.Out(m.Bit))

main = m.DefineCircuit("main", "I", m.In(m.Bits[2]), "O", m.Out(m.Bit))

and2 = And2()

m.wire(main.I[0], and2.I0)
m.wire(main.I[1], and2.I1)
m.wire(and2.O, main.O)

m.EndCircuit()

m.compile("main", main, output="coreir-verilog")
```

run with `python main.py` to produce

```json
{"top":"global.main",
"namespaces":{
  "global":{
    "modules":{
      "And2":{
        "type":["Record",[
          ["I0","BitIn"],
          ["I1","BitIn"],
          ["O","Bit"]
        ]],
        "metadata":{"filename":"main.py","lineno":"6"}
      },
      "main":{
        "type":["Record",[
          ["I",["Array",2,"BitIn"]],
          ["O","Bit"]
        ]],
        "instances":{
          "And2_inst0":{
            "modref":"global.And2",
            "metadata":{"filename":"main.py","lineno":"10"}
          }
        },
        "connections":[
          ["self.I.0","And2_inst0.I0",{"filename":"main.py","lineno":"12"}],
          ["self.I.1","And2_inst0.I1",{"filename":"main.py","lineno":"13"}],
          ["self.O","And2_inst0.O",{"filename":"main.py","lineno":"14"}]
        ],
        "metadata":{"filename":"main.py","lineno":"8"}
      }
    }
  }
}
}
```
