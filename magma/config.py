__COMPILE_DIR = 'normal'


def set_compile_dir(target):
    global __COMPILE_DIR
    assert target in ['normal', 'callee_file_dir']
    __COMPILE_DIR = target


def get_compile_dir():
    return __COMPILE_DIR


__DEBUG_MODE = False


def set_debug_mode(value=True):
    global __DEBUG_MODE
    assert value in {True, False}
    __DEBUG_MODE = value


def get_debug_mode():
    return __DEBUG_MODE
