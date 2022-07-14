import magma as m


class Ext(m.Generator2):
    def __init__(self, width_a: int, width_b: int):
        self.io = m.IO(**{
            "a": m.In(m.Bits[width_a]),
            "b": m.In(m.Bits[width_b]),
            "O": m.Out(m.Bits[32]),
        })
        self.coreir_config_param_types = {
            "width_a": int,
            "width_b": int,
        }
        self.width_a = width_a
        self.width_b = width_b
        #self.name = f"Ext_{width_a}_{width_b}"
        self.coreir_metadata = {"verilog_name": "Ext"}

    @property
    def name(self):
        return f"Ext_{self.width_a}_{self.width_b}"


class Top(m.Circuit):
    io = m.IO(I=m.In(m.Bits[32]), O=m.Out(m.Bits[32]))
    x = Ext(24, 8)(width_a=24, width_b=8)(io.I[:24], io.I[24:])
    y = Ext(25, 7)(width_a=25, width_b=7)(io.I[:25], io.I[25:])

    e = Ext(24, 8)
    import inspect
    print (inspect.signature(e.__class__.__init__))
    
    io.O @= x | y


opts = {
    "output": "mlir-verilog",
}
m.compile("top", Top, **opts)
