__COMPILE_DIR = 'normal'


def set_compile_dir(target):
    global __COMPILE_DIR
    assert target in ['normal', 'callee_file_dir']
    __COMPILE_DIR = target


def get_compile_dir():
    return __COMPILE_DIR
