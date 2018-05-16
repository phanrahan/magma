import os
import warnings

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

cachedFunctions = []
def clear_cachedFunctions():
    for func in cachedFunctions:
        func.cache_clear()

def cache_definition(fn):
    cachedFunctions.append(lru_cache(maxsize=None)(fn))
    return cachedFunctions[-1]

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

from .frontend.coreir_ import DeclareCoreIRGenerator, coreir_typegen
