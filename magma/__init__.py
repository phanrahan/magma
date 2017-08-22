import os

# utility
# from .bits import *
# from .bitwise import *

# lowest-level wiring abstraction
from .port import *

# types
from .t import *
from .bit import *
from .bitutils import *
from .array import *
from .bits import *
from .tuple import *
from .interface import *
from .primitives import *
from .conversions import *

from .wire import *
from .circuit import *

from .peripheral import *
from .part import *
from .fpga import *

from .board import *

# verilog 
from .fromverilog import *
from .backend.verilog import *

from .higher import *

if os.getenv("MAGMA_COMPILE_STYLE") == "abstract":
    from .compile_abstract import *
else:
    from .compile import *

from .tests import *

#print('import magma')
