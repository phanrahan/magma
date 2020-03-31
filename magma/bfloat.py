from functools import lru_cache
from magma.bit import Bit
from magma.bits import UInt
from magma.circuit import DeclareCoreirCircuit
from magma.t import In, Out


class BFloat(UInt):
    @classmethod
    @lru_cache(maxsize=None)
    def declare_unary_op(cls, op):
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")
        coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
        return DeclareCoreirCircuit(f"magma_BFloat_{N}_{op}",
                                    "I", In(cls),
                                    "O", Out(cls),
                                    coreir_name=op,
                                    coreir_genargs=coreir_genargs,
                                    coreir_lib="float")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_binary_op(cls, op):
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")
        coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
        return DeclareCoreirCircuit(f"magma_BFloat_{N}_{op}",
                                    "I0", In(cls),
                                    "I1", In(cls),
                                    "O", Out(cls),
                                    coreir_name=op,
                                    coreir_genargs=coreir_genargs,
                                    coreir_lib="float")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_compare_op(cls, op):
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")
        coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
        return DeclareCoreirCircuit(f"magma_BFloat_{N}_{op}",
                                    "I0", In(cls),
                                    "I1", In(cls),
                                    "O", Out(Bit),
                                    coreir_name=op,
                                    coreir_genargs=coreir_genargs,
                                    coreir_lib="float")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_ite(cls, T):
        t_str = str(T)
        # Sanitize
        t_str = t_str.replace("(", "_")
        t_str = t_str.replace(")", "")
        t_str = t_str.replace("[", "_")
        t_str = t_str.replace("]", "")
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")
        coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
        return DeclareCoreirCircuit(f"magma_BFloat_{N}_ite_{t_str}",
                                    "I0", In(T),
                                    "I1", In(T),
                                    "S", In(Bit),
                                    "O", Out(T),
                                    coreir_name="mux",
                                    coreir_genargs=coreir_genargs,
                                    coreir_lib="float")
