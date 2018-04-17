import os
import warnings

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

def cache_definition(fn):
    warnings.warn("deprecated, circuit definition caching now based on "
                  "names", DeprecationWarning)
    return fn
    #return lru_cache(maxsize=None)(fn)

# lowest-level wiring abstraction
from .port import *

# types
from .t import *
from .bit import *
#from .bitutils import *
from .array import *
from .bits import *
from .tuple import *
from .clock import *
from .conversions import *
from .interface import *

from .circuit import *
from .braid import *

from .wire import *

# verilog
from .fromverilog import *
from .backend.verilog import *
from .compile import *

#from .tests import *

#print('import magma')
