import dataclasses


@dataclasses.dataclass(frozen=True)
class CompileToMlirOpts:
    flatten_all_tuples: bool = False
