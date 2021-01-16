from coreir import Context


_coreir_context = Context()
_module_map = {}  # map from context to modules


def coreir_context():
    global _coreir_context
    return _coreir_context


def reset_coreir_context():
    global _coreir_context
    global _module_map
    try:
        del _module_map[_coreir_context]
    except KeyError:  # _coreir_context (singleton) not mapped
        pass
    _coreir_context.delete()
    _coreir_context = Context()


def module_map():
    global _module_map
    return _module_map
