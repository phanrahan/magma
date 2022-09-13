from typing import Dict, Optional

from magma.circuit import get_instance_callback
from magma.passes.passes import InstancePass


class InstanceCallbackPass(InstancePass):
    def __init__(self, main, data: Optional[Dict]):
        super().__init__(main)
        if data is None:
            data = {}
        self.data = data

    def __call__(self, path):
        inst = path[-1]
        try:
            callback = get_instance_callback(inst)
        except AttributeError:
            return
        path = [self.main] + list(path)
        callback(path, self.data)


def instance_callback_pass(main, data: Optional[Dict] = None):
    p = InstanceCallbackPass(main, data)
    p.run()
    return p.data
