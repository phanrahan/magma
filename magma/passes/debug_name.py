import gc
from .passes import DefinitionPass

__all__ = ['DebugNamePass']


class InstDecl:
    def __init__(self, varname, lineno, filename):
        self.varname = varname
        self.lineno = lineno
        self.filename = filename

    def __repr__(self):
        return f"{self.filename} line {self.lineno}: {self.varname}"


def _create_debugname(ref_name, ref, inst):
    if ref is inst:
        return ref_name
    if isinstance(ref, list):
        idx = ref.index(inst)
        return f"{ref_name}[{idx}]"
    return ref_name


class DebugNamePass(DefinitionPass):
    def __call__(self, definition):
        for inst in definition.instances:
            referrers = gc.get_referrers(inst)
            # Skip if this pass has already been run (partially or not).
            if hasattr(inst, "decl"):
                continue
            stack = inst.stack
            inst.decl = None
            # Skip the first element in the stack, where the inst is placed.
            for frame_info in stack[1:]:
                local_vars = frame_info[0].f_locals.items()
                for name, var in local_vars:
                    if any(var is x for x in referrers) or var is inst:
                        debugname = _create_debugname(name, var, inst)
                        # Ignore the 'self' frame (where the inst is created).
                        if debugname == "self":
                            break
                        lineno = frame_info[2]
                        filename = frame_info[0].f_code.co_filename
                        inst.decl = InstDecl(debugname, lineno, filename)
                        break
