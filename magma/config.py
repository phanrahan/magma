__COMPILE_DIR = 'normal'


def set_compile_dir(target):
    global __COMPILE_DIR
    assert target in ['normal', 'callee_file_dir']
    __COMPILE_DIR = target


def get_compile_dir():
    return __COMPILE_DIR


__database_hash_backend = "coreir"


def set_database_hash_backend(target):
    global __database_hash_backend
    assert target in ["verilog", "coreir"]
    __database_hash_backend = target


def get_database_hash_backend():
    return __database_hash_backend
