import magma as m

from common import make_unique_name


def _make_type_string(T: m.Kind):
    _REPLACEMENTS = (
        ("(", "_"), (")", ""), ("[", "_"), ("]", ""), (" ", ""), (",", "_"))
    s = str(T)
    for old, new in _REPLACEMENTS:
        s = s.replace(old, new)
    return s


def make_instance(defn: m.circuit.CircuitKind) -> m.Circuit:
    insts = []

    class _(m.Circuit):
        i = defn(name=make_unique_name())
        insts.append(i)

    return insts[0]


class MagmaArrayGetOp(m.Generator2):
    def __init__(self, T: m.ArrayMeta, index: int):
        assert isinstance(T, m.ArrayMeta)
        T = T.undirected_t
        self.name = f"magma_array_get_op_{_make_type_string(T)}_{index}"
        self.primitive = True

        T_out = T.T
        self.io = m.IO(I=m.In(T), O=m.Out(T_out))

        self.T = T
        self.index = index


class MagmaArraySliceOp(m.Generator2):
    def __init__(self, T: m.ArrayMeta, lo: int, hi: int):
        assert isinstance(T, m.ArrayMeta)
        T = T.undirected_t
        self.name = f"magma_array_slice_op_{_make_type_string(T)}_{lo}_{hi}"
        self.primitive = True

        T_out = T.unsized_t[hi - lo]
        self.io = m.IO(I=m.In(T), O=m.Out(T_out))

        self.T = T
        self.lo = lo
        self.hi = hi


class MagmaArrayCreateOp(m.Generator2):
    def __init__(self, T: m.ArrayMeta):
        assert isinstance(T, m.ArrayMeta)
        T = T.undirected_t
        self.name = f"magma_array_create_op_{_make_type_string(T)}"
        self.primitive = True

        self.io = (m.IO(**{f"I{i}": m.In(T.T) for i in range(T.N)}) +
                   m.IO(O=m.Out(T)))
        self.T = T
