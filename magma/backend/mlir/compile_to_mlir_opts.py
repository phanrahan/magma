import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class CompileToMlirOpts:
    flatten_all_tuples: bool = False
    basename: Optional[str] = None
    use_native_bind_processor: bool = False
    verilog_prefix: Optional[str] = None
    user_namespace: Optional[str] = None
