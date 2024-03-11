from magma.config import config as magma_config


def pytest_configure(config):
    magma_config.compile_dir = 'callee_file_dir'
    # TODO(leonardt): Enable this globally for testing
    # Revert a3a2452168f2251277a14548d053a9ca7a45bff7 for golds.
    #
    # magma_config.use_namer_dict = True
    magma_config.use_uinspect = True
