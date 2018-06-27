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


# wires
from .port import *
from .wire import *

# types
from .t import *
from .bit import *
from .array import *
from .bits import *
from .tuple import *
from .clock import *
from .conversions import *
from .interface import *

# circuit
from .circuit import *

# higher-order operators
from .braid import *

# verilog
from .fromverilog import *
from .backend.verilog import *

# compile
from .compile import *

from .logging import warning


mantle_target = None
def set_mantle_target(t):
     global mantle_target
     if mantle_target is not None and mantle_target != t:
         warning('changing mantle target', mantle_target, t )
     mantle_target = t
 
