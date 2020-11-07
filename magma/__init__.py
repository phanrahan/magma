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

def singleton(cls):
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper

from magma.protocol_type import MagmaProtocolMeta, MagmaProtocol

# wires
from .wire import wire

# types
from .t import *

from .bit import *

from .array import *
from .bits import *
from .bfloat import BFloat
from .tuple import *
from .clock import *
from .clock_io import ClockIO
from .conversions import *
from .interface import *
from .ref import LazyDefnRef, LazyInstRef

# circuit
from .circuit import *

# higher-order operators
from .braid import *

# verilog
from .frontend.verilog import (declare_from_verilog, declare_from_verilog_file,
                               define_from_verilog, define_from_verilog_file,
                               DeclareFromVerilog, DeclareFromVerilogFile,
                               DefineFromVerilog, DefineFromVerilogFile,
                               set_verilog_importer)
from .backend.verilog import *

# compile
from .compile import *

from .logging import root_logger


mantle_target = None
def set_mantle_target(t):
     global mantle_target
     if mantle_target is not None and mantle_target != t:
         root_logger().warning('changing mantle target', mantle_target, t )
     mantle_target = t

from .backend.util import set_codegen_debug_info
from .enum import Enum
import magma.util
import magma.syntax

from .is_primitive import isprimitive
from .is_definition import isdefinition

from .uniquification import UniquificationPass


from hwtypes.bit_vector_abc import TypeFamily

from magma.family import get_family
_Family_ = get_family()

from .generator import Generator, Generator2
from .monitor import MonitorIO, MonitorGenerator, make_monitor_ports
from .inline_verilog import inline_verilog
from .display import display, posedge, negedge, File, time
from .log import info, debug, warning, error


from .syntax.sequential2 import sequential2
from .syntax.combinational2 import combinational2
from .syntax.inline_combinational import inline_combinational
from .syntax.coroutine import coroutine

from magma.primitives import (LUT, Mux, mux, dict_lookup, list_lookup,
                              Register, get_slice, set_slice, slice,
                              Memory, set_index, register)

from magma.types import (BitPattern, Valid, ReadyValid, Consumer, Producer,
                         Decoupled, EnqIO, DeqIO, Irrevocable)
import magma.smart
