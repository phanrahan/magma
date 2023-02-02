import magma as m


def test_config_debug():
    def _check(val: bool):
        m.config.config.debug_mode = val
        for field in ["use_uinspect", "use_namer_dict", "debug_mode"]:
            assert getattr(m.config.config, field) is val

    for val in [True, False]:
        _check(val)

    # Reset default
    m.config.config.use_uinspect = True
