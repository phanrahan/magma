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


def make_unused_undriven(bit_def, bits_def, attr):
    def make_func(T):
        if issubclass(T, m.Bit):
            return getattr(bit_def()(), attr)
        elif issubclass(T, m.Array) and issubclass(T.T, m.Digital):
            return getattr(bits_def(len(T))(), attr)
        elif issubclass(T, m.Array):
            return m.array([make_func(T.T) for _ in range(len(T))])
        elif issubclass(T, m.Product):
            return m.namedtuple(
                **{key: make_func(value) for key, value in T.field_dict.items()}
            )
        elif issubclass(T, m.Tuple):
            return m.tuple_(
                [make_func(t) for t in T.fields]
            )
        else:
            raise NotImplementedError(T)
    return make_func


make_Unused = make_unused_undriven(DefineCorebitTerm, DefineTerm, "I")
make_Undriven = make_unused_undriven(DefineCorebitUndriven, DefineUndriven, "O")


class Undriven:
    pass


class Unused:
    def __imatmul__(self, other):
        m.wire(make_Unused(type(other)), other)
        return self


# Singleton hack to use __imatmul__ impl
Unused = Unused()


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
