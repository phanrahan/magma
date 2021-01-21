from coreir import Context


class _CompilerCache:
    def __init__(self):
        self._cache = {}

    @staticmethod
    def _make_key(context, namespace, magma_module):
        return (id(context), namespace, id(magma_module))

    def get(self, context, namespace, magma_module):
        key = _CompilerCache._make_key(context, namespace, magma_module)
        return self._cache[key]

    def set(self, context, namespace, magma_module, coreir_module):
        key = _CompilerCache._make_key(context, namespace, magma_module)
        self._cache[key] = coreir_module


_coreir_context = Context()
_compiler_cache = _CompilerCache()


def coreir_context():
    global _coreir_context
    return _coreir_context


def reset_coreir_context():
    global _coreir_context
    _coreir_context.delete()
    _coreir_context = Context()


def compiler_cache():
    global _compiler_cache
    return _compiler_cache
