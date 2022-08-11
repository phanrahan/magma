import dataclasses
from typing import Dict, Optional, Set

from magma.circuit import Circuit
from magma.digital import Digital
from magma.generator import Generator2
from magma.interface import IO
from magma.t import Type
from magma.when import (
    BlockBase as WhenBlock,
    get_all_blocks as get_all_when_blocks,
)
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
    for conditional_wire in block.conditional_wires():
        info.add_input(conditional_wire.drivee)
        info.add_output(conditional_wire.driver)
    for wire in block.default_drivers():
        info.add_default_driver(wire.drivee, wire.driver)


class When(Generator2):
    _cache_ = False

    def __init__(self, block: WhenBlock):
        self._block = block

        self._info = info = _BlockInfo()
        for block in get_all_when_blocks(block):
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

        self.name = f"When_{id(self._block)}"
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
