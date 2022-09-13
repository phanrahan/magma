import pytest

import magma as m


@pytest.mark.parametrize("use_lambda", (False, True))
def test_basic(use_lambda):

    def _callback(path, data):
        data[0] = path

    class _Test(m.Circuit):
        reg = m.Register(m.Bit)(name="r")
        m.register_instance_callback(reg, _callback)

    if use_lambda:
        data = m.passes.instance_callback_pass(_Test)
    else:
        p = m.passes.InstanceCallbackPass(_Test, None)
        p.run()
        data = p.data

    assert data == {0: [_Test, _Test.reg]}
