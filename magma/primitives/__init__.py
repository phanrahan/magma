import os
from magma.bit import BitType

mode = os.environ.get("MAGMA_PRIMITIVES", "FIRRTL")


if mode == "FIRRTL":
    import magma.primitives.firrtl
else:
    raise NotImplementedError()
