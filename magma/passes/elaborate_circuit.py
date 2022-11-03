from magma.circuit import CircuitKind
from magma.passes.passes import CircuitPass, pass_lambda


def elaborate_circuit(ckt: CircuitKind):
    with ckt.open():
        ckt.elaborate()
    if getattr(ckt, "primitive", False):
        setattr(ckt, "primitive", False)
    ckt._is_definition = True


class ElaborationPass(CircuitPass):
    def __init__(self, main):
        super().__init__(main)

    def should_elaborate(self, ckt):
        raise NotImplementedError()

    def __call__(self, ckt):
        if self.should_elaborate(ckt):
            elaborate_circuit(ckt)


class ElaborateAllPass(ElaborationPass):
    def __init__(self, main, circuits=(), generators=()):
        super().__init__(main)
        self._circuits = circuits
        self._generators = generators

    def should_elaborate(self, ckt):
        # NOTE(rsetaluri): We are using a subclass check for circuits. This is
        # not necessarily guaranteed to be equivalent to checking that the
        # instance itself isinstance of the circuit, but we can expect it to
        # work for most cases.
        return (
            issubclass(ckt, self._circuits)
            or isinstance(ckt, self._generators)
        )


elaborate_all_pass = pass_lambda(ElaborateAllPass)
