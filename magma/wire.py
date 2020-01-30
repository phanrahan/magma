import magma as m
from .compatibility import IntegerTypes
from .debug import debug_wire
from .logging import root_logger


_logger = root_logger()


def DefineUndriven(width):
    def simulate_undriven(self, value_store, state_store):
        pass
    return m.circuit.DeclareCoreirCircuit(
        f"undriven",
        "O", m.Out(m.Bits[width]),
        coreir_name="undriven",
        coreir_lib="coreir",
        coreir_genargs={"width": width},
        simulate=simulate_undriven
    )


def DefineCorebitUndriven():
    def simulate_corebit_undriven(self, value_store, state_store):
        pass
    return m.circuit.DeclareCoreirCircuit(
        f"corebit_undriven",
        "O", m.Out(m.Bit),
        coreir_name="undriven",
        coreir_lib="corebit",
        simulate=simulate_corebit_undriven
    )


def DefineTerm(width):
    def simulate_term(self, value_store, state_store):
        pass
    return m.circuit.DeclareCoreirCircuit(
        f"term",
        "I", m.In(m.Bits[width]),
        coreir_name="term",
        coreir_lib="coreir",
        coreir_genargs={"width": width},
        simulate=simulate_term
    )


def DefineCorebitTerm():
    def simulate_corebit_term(self, value_store, state_store):
        pass
    return m.circuit.DeclareCoreirCircuit(
        f"corebit_term",
        "I", m.In(m.Bit),
        coreir_name="term",
        coreir_lib="corebit",
        simulate=simulate_corebit_term
    )


class Undriven:
    pass


def make_Unused(T):
    if issubclass(T, m.Bit):
        return DefineCorebitTerm()().I
    elif issubclass(T, m.Array) and issubclass(T.T, m.Digital):
        return DefineTerm(len(T))().I
    elif issubclass(T, m.Array):
        return m.array([make_Unused(T.T) for _ in range(len(T))])
    elif issubclass(T, m.Product):
        return m.namedtuple(
            **{key: make_Unused(value) for key, value in T.field_dict.items()}
        )
    elif issubclass(T, m.Tuple):
        return m.tuple_(
            [make_Unused(t) for t in T.fields]
        )
    else:
        raise NotImplementedError(T)


class Unused:
    def __imatmul__(self, other):
        m.wire(make_Unused(type(other)), other)
        return self


# Singleton hack to use __imatmul__ impl
Unused = Unused()


def make_Undriven(T):
    if issubclass(T, m.Bit):
        return DefineCorebitUndriven()().O
    elif issubclass(T, m.Array) and issubclass(T.T, m.Digital):
        return DefineUndriven(len(T))().O
    elif issubclass(T, m.Array):
        return m.array([make_Undriven(T.T) for _ in range(len(T))])
    elif issubclass(T, m.Product):
        return m.namedtuple(
            **{key: make_Undriven(value) for key, value in T.field_dict.items()}
        )
    elif issubclass(T, m.Tuple):
        return m.tuple_(
            [make_Undriven(t) for t in T.fields]
        )
    else:
        raise NotImplementedError(T)

@debug_wire
def wire(o, i, debug_info=None):
    if i is Undriven:
        i = make_Undriven(type(o))

    # Wire(o, Circuit).
    if hasattr(i, 'interface'):
        i.wire(o, debug_info)
        return

    # Replace output Circuit with its output (should only be 1 output).
    if hasattr(o, 'interface'):
        # If wiring a Circuit to a Port then circuit should have 1 output.
        o_orig = o
        o = o.interface.outputs()
        if len(o) != 1:
            _logger.error(f"Can only wire circuits with one output. Argument "
                          f"0 to wire `{o_orig.debug_name}` has outputs {o}",
                          debug_info=debug_info)
            return
        o = o[0]

    # If o is an input.
    if not isinstance(o, IntegerTypes) and o.is_input():
        # If i is not an input.
        if isinstance(i, IntegerTypes) or not i.is_input():
            # Flip i and o.
            i, o = o, i

    # Wire(o, Type).
    i.wire(o, debug_info)
