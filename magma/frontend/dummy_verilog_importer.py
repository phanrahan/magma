from magma.frontend.verilog_importer import VerilogImporter


class DummyVerilogImporter(VerilogImporter):
    def __init__(self):
        super().__init__({})

    def import_(self, src, mode):
        raise NotImplementedError()
