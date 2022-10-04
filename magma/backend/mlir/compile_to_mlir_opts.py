import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class CompileToMlirOpts:
    flatten_all_tuples: bool = False
    basename: Optional[str] = None
    use_native_bind_processor: bool = False
    verilog_prefix: Optional[str] = None
    user_namespace: Optional[str] = None
    disable_initial_blocks: bool = False
    elaborate_magma_registers: bool = False
    extend_non_power_of_two_muxes: bool = False
    disallow_duplicate_symbols: bool = False
