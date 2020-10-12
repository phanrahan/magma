from functools import lru_cache
from magma.bit import Bit
from magma.bits import UInt
from magma.circuit import Circuit, coreir_port_mapping
from magma.interface import IO
from magma.t import In, Out


class CoreIRFloatOp(Circuit):
    renamed_ports = coreir_port_mapping
    coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
    coreir_lib = "float"


class BFloat(UInt):
    @classmethod
    @lru_cache(maxsize=None)
    def declare_unary_op(cls, op):
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")

        class _BFloatOp(CoreIRFloatOp):
            # Have to explicitly inherit class variables, but at least we can
            # keep one copy if we ever have to change them
            renamed_ports = CoreIRFloatOp.renamed_ports
            coreir_genargs = CoreIRFloatOp.coreir_genargs
            coreir_lib = CoreIRFloatOp.coreir_lib

            name = f"magma_BFloat_{N}_{op}"
            io = IO(I=In(cls), O=Out(cls))
            coreir_name = op
        return _BFloatOp

    @classmethod
    @lru_cache(maxsize=None)
    def declare_binary_op(cls, op):
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")

        class _BFloatOp(CoreIRFloatOp):
            renamed_ports = CoreIRFloatOp.renamed_ports
            coreir_genargs = CoreIRFloatOp.coreir_genargs
            coreir_lib = CoreIRFloatOp.coreir_lib

            name = f"magma_BFloat_{N}_{op}"
            io = IO(I0=In(cls), I1=In(cls), O=Out(cls))
            coreir_name = op
            coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
            coreir_lib = "float"
        return _BFloatOp

    @classmethod
    @lru_cache(maxsize=None)
    def declare_compare_op(cls, op):
        N = len(cls)
        if N != 16:
            raise NotImplementedError("Only BFloat16 supported")

        class _BFloatOp(CoreIRFloatOp):
            renamed_ports = CoreIRFloatOp.renamed_ports
            coreir_genargs = CoreIRFloatOp.coreir_genargs
            coreir_lib = CoreIRFloatOp.coreir_lib

            name = f"magma_BFloat_{N}_{op}"
            io = IO(I0=In(cls), I1=In(cls), O=Out(Bit))
            coreir_name = op
            coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
            coreir_lib = "float"
        return _BFloatOp

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

        class _BFloatOp(CoreIRFloatOp):
            renamed_ports = CoreIRFloatOp.renamed_ports
            coreir_genargs = CoreIRFloatOp.coreir_genargs
            coreir_lib = CoreIRFloatOp.coreir_lib

            name = f"magma_BFloat_{N}_ite_{t_str}"
            io = IO(I0=T, I1=T, S=In(Bit), O=Out(T))
            coreir_name = "mux"
            coreir_genargs = {"exp_bits": 8, "frac_bits": 7}
            coreir_lib = "float"
        return _BFloatOp
