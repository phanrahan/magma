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
# Define default operators that raise exceptions, rename so it doesn't muck
# with `from magma import *` code that also uses operator
import magma.operators
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

from .backend.util import set_codegen_debug_info
from .enum import Enum
import magma.util

from .is_primitive import isprimitive
from .is_definition import isdefinition

from .product import Product


from hwtypes.bit_vector_abc import TypeFamily


BitVector = Bits
UIntVector = UInt
SIntVector = SInt
_Family_ = TypeFamily(Bit, BitVector, UIntVector, SIntVector)
def get_family():
    return _Family_
