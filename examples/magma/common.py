import sys
import tempfile

import magma as m


def _try_pop(dct, key, default):
    try:
        return dct.pop(key)
    except KeyError:
        return default


def print_verilog(ckt, **opts):
    sout = _try_pop(opts, "sout", sys.stderr)
    print_ir = _try_pop(opts, "print_ir", False)
    with tempfile.TemporaryDirectory() as directory:
        design_basename = f"{directory}/design"
        m.compile(design_basename, ckt, **opts)
        if print_ir:
            with open(f"{directory}/design.json", "r") as f:
                ir = f.read()
        with open(f"{directory}/design.v", "r") as f:
            verilog = f.read()
    if print_ir:
        print (ir, file=sout)
    print (verilog, file=sout)
