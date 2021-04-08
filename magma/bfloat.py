from functools import lru_cache, wraps
from magma.bit import Bit
from magma.bits import UInt
from magma.circuit import declare_coreir_circuit
from magma.t import In, Out


def _declare_bfloat_circuit(name: str, ports: dict, coreir_name: str):
    return declare_coreir_circuit(name, ports, coreir_name,
                                  {"exp_bits": 8, "frac_bits": 7}, "float")


def check_len(fn):
    @wraps(fn)
    def wrapper(cls, op):
        if len(cls) != 16:
            raise NotImplementedError("Only BFloat16 supported")
        return fn(cls, op)
    return wrapper


class BFloat(UInt):
    @classmethod
    @lru_cache(maxsize=None)
    @check_len
    def _declare_unary_op(cls, op):
        return _declare_bfloat_circuit(f"magma_BFloat_{len(cls)}_{op}",
                                       {"I": In(cls), "O": Out(cls)}, op)

    @classmethod
    @lru_cache(maxsize=None)
    @check_len
    def _declare_binary_op(cls, op):
        return _declare_bfloat_circuit(f"magma_BFloat_{len(cls)}_{op}",
                                       {"I0": In(cls), "I1": In(cls),
                                        "O": Out(cls)}, op)

    @classmethod
    @lru_cache(maxsize=None)
    @check_len
    def _declare_compare_op(cls, op):
        return _declare_bfloat_circuit(f"magma_BFloat_{len(cls)}_{op}",
                                       {"I0", In(cls), "I1", In(cls),
                                        "O", Out(Bit)}, op)

    @classmethod
    @lru_cache(maxsize=None)
    @check_len
    def _declare_ite(cls, T):
        t_str = str(T)
        # Sanitize
        t_str = t_str.replace("(", "_")
        t_str = t_str.replace(")", "")
        t_str = t_str.replace("[", "_")
        t_str = t_str.replace("]", "")
        return _declare_bfloat_circuit(f"magma_BFloat_{len(cls)}_ite_{t_str}",
                                       {"I0": In(T), "I1": In(T),
                                        "S": In(Bit), "O": Out(T)}, "mux")
