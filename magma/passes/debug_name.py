from .passes import DefinitionPass

__all__ = ['DebugNamePass']

class InstDecl:
    def __init__(self, varname, lineno, filename):
        self.varname = varname
        self.lineno = lineno
        self.filename = filename

    def __repr__(self):
        return self.filename + " line " + str(self.lineno) + ": " + self.varname

class DebugNamePass(DefinitionPass):
    def __call__(self, definition):
        for inst in definition.instances:
            if hasattr(inst, 'decl'):
                # Skip if this pass has already been run (partially or not)
                continue
            stack = inst.stack
            inst.decl = None
            for frame_info in stack:
                local_vars = frame_info.frame.f_locals.items()
                for name, var in local_vars:
                    if var is inst:
                        inst.decl = InstDecl(name, frame_info.lineno, frame_info.frame.f_code.co_filename)
                        break
