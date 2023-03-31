import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class CompileToMlirOpts:
    flatten_all_tuples: bool = False
    basename: Optional[str] = None
    sv: bool = False
    use_native_bind_processor: bool = False
    verilog_prefix: Optional[str] = None
    user_namespace: Optional[str] = None
    disable_initial_blocks: bool = False
    elaborate_magma_registers: bool = False
    extend_non_power_of_two_muxes: bool = False
    disallow_duplicate_symbols: bool = False
    location_info_style: str = "none"
    explicit_bitcast: bool = False
    disallow_expression_inlining_in_ports: bool = False
    disallow_local_variables: bool = False
    split_verilog: bool = False
    omit_version_comment: bool = False
