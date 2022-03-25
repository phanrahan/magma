import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class CompileToMlirOpts:
    flatten_all_tuples: bool = False
    basename: Optional[str] = None
