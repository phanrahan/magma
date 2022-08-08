import dataclasses
from typing import Dict, Optional, Set

from magma.circuit import Circuit
from magma.digital import Digital
from magma.generator import Generator2
from magma.interface import IO
from magma.t import Type
from magma.when import BlockBase as WhenBlock
from magma.wire import wire


def _empty_dict_field():
    return dataclasses.field(default_factory=dict, init=False)


@dataclasses.dataclass
class _BlockInfo:
    inputs: Dict[Type, int] = _empty_dict_field()
    outputs: Dict[Type, int] = _empty_dict_field()
    conditions: Dict[Type, int] = _empty_dict_field()
    default_drivers: Dict[Type, Type] = _empty_dict_field()

    @staticmethod
    def _generic_add(dct: Dict[Type, int], value: Optional[Type]):
        if value is None:
            return
        dct.setdefault(value, len(dct))

    def add_input(self, value: Type):
        _BlockInfo._generic_add(self.inputs, value)

    def add_output(self, value: Type):
        _BlockInfo._generic_add(self.outputs, value)

    def add_condition(self, condition: Optional[Digital]):
        _BlockInfo._generic_add(self.conditions, condition)

    def add_default_driver(self, drivee: Type, driver: Type):
        self.add_output(driver)
        self.default_drivers[drivee] = driver


def _construct_block_info(block: WhenBlock, info: _BlockInfo):
    info.add_condition(block.condition)
    for i, o in block.conditional_wires():
        info.add_input(i)
        if i.driven():
            driver = i.value()
            info.add_default_driver(i, driver)
            i.unwire(driver)
        info.add_output(o)
    for child in block.children():
        _construct_block_info(child, info)
    for elsewhen_block in block.elsewhen_blocks():
        _construct_block_info(elsewhen_block, info)
    if block.otherwise_block is not None:
        _construct_block_info(block.otherwise_block, info)


class When(Generator2):
    def __init__(self, block: WhenBlock):
        self._block = block

        self._info = info = _BlockInfo()
        _construct_block_info(block, info)

        ports = {}
        self._wire_map = wire_map = {}
        for value, i in info.conditions.items():
            ports.update({f"S{i}": type(value).flip()})
            wire_map[value] = f"S{i}"
        for i, value in enumerate(info.outputs):
            ports.update({f"I{i}": type(value).flip()})
            wire_map[value] = f"I{i}"
        for i, value in enumerate(info.inputs):
            ports.update({f"O{i}": type(value).flip()})
            wire_map[value] = f"O{i}"

        self.io = io = IO(**ports)

        self.name = f"When_{id(block)}"
        self.primitive = True

    @property
    def block(self) -> WhenBlock:
        return self._block

    @property
    def info(self) -> _BlockInfo:
        return self._info

    def wire_instance(self, inst):
        for value, port_name in self._wire_map.items():
            wire(value, getattr(inst, port_name))
