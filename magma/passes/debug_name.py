import gc
from .passes import DefinitionPass

__all__ = ['DebugNamePass']

class InstDecl:
    def __init__(self, varname, lineno, filename):
        self.varname = varname
        self.lineno = lineno
        self.filename = filename

    def __repr__(self):
        return self.filename + " line " + str(self.lineno) + ": " + self.varname

def create_debugname(ref_name, ref, inst):
    if ref is inst:
        return ref_name

    if isinstance(ref, list):
        idx = ref.index(inst)
        return "{}[{}]".format(ref_name, idx)

    return ref_name

class DebugNamePass(DefinitionPass):
    def __call__(self, definition):
        for inst in definition.instances:
            referrers = gc.get_referrers(inst)

            if hasattr(inst, 'decl'):
                # Skip if this pass has already been run (partially or not)
                continue
            stack = inst.stack
            inst.decl = None
            for frame_info in stack[1:]: # Skip the first element in the stack, where the inst is placed
                local_vars = frame_info[0].f_locals.items()
                for name, var in local_vars:
                    if any(var is x for x in referrers) or var is inst:
                        debugname = create_debugname(name, var, inst)

                        # Ignore the 'self' frame (where the inst is created)
                        if debugname == 'self':
                            break

                        inst.decl = InstDecl(debugname, frame_info[2], frame_info[0].f_code.co_filename)
                        break
