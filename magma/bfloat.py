import magma as m
from .bits import UInt
from functools import lru_cache


class BFloat(UInt):
    @classmethod
    @lru_cache(maxsize=None)
    def declare_unary_op(cls, op):
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")
        coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
        return m.circuit.DeclareCoreirCircuit(f"magma_BFloat_{N}_{op}",
                                              "I", m.In(cls),
                                              "O", m.Out(cls),
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
        return m.circuit.DeclareCoreirCircuit(f"magma_BFloat_{N}_{op}",
                                              "I0", m.In(cls),
                                              "I1", m.In(cls),
                                              "O", m.Out(cls),
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
        return m.circuit.DeclareCoreirCircuit(f"magma_BFloat_{N}_{op}",
                                              "I0", m.In(cls),
                                              "I1", m.In(cls),
                                              "O", m.Out(m.Bit),
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
        return m.circuit.DeclareCoreirCircuit(f"magma_BFloat_{N}_ite_{t_str}",
                                              "I0", m.In(T),
                                              "I1", m.In(T),
                                              "S", m.In(m.Bit),
                                              "O", m.Out(T),
                                              coreir_name="mux",
                                              coreir_genargs=coreir_genargs,
                                              coreir_lib="float")
