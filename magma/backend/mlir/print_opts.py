import dataclasses


@dataclasses.dataclass(frozen=True)
class PrintOpts:
    print_locations: bool = False
