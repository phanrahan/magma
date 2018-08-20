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
