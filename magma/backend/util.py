from collections import defaultdict
import os


__magma_codegen_debug_info = False
if os.environ.get("MAGMA_CODEGEN_DEBUG_INFO", False):
    __magma_codegen_debug_info = True


def set_codegen_debug_info(val):
    global __magma_codegen_debug_info
    __magma_codegen_debug_info = val


def get_codegen_debug_info():
    return __magma_codegen_debug_info


def make_relative(path):
    cwd = os.getcwd()
    common_prefix = os.path.commonprefix([cwd, path])
    return os.path.relpath(path, common_prefix)


class keydefaultdict(defaultdict):
    """See: https://stackoverflow.com/questions/2912231/is-there-a-clever-way-to-pass-the-key-to-defaultdicts-default-factory"""  # noqa
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )  # pragma: no cover
        else:
            ret = self[key] = self.default_factory(key)
            return ret
