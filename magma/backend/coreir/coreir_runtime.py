from coreir import Context


_coreir_context = Context()
_namespace_module_map = {}  # map from context to namespaces to modules


def coreir_context():
    global _coreir_context
    return _coreir_context


def reset_coreir_context():
    global _coreir_context
    global _namespace_module_map
    try:
        del _namespace_module_map[_coreir_context]
    except KeyError:  # _coreir_context (singleton) not mapped
        pass
    _coreir_context.delete()
    _coreir_context = Context()


def namespace_module_map():
    global _namespace_module_map
    return _namespace_module_map
