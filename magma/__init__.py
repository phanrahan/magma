import os

# lowest-level wiring abstraction
from .port import *

# types
from .t import *
from .bit import *
from .bitutils import *
from .array import *
from .bits import *
from .tuple import *
from .clock import *
from .conversions import *
from .interface import *

from .circuit import *
from .wire import *
from .higher import *

from .primitives import *

# verilog 
from .fromverilog import *
from .backend.verilog import *
from .compile import *

from .tests import *

coreir_primitives_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "coreir_prims.v")

#print('import magma')
