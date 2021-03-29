import pytest

from magma.symbol_table import SymbolTable, SYMBOL_TABLE_EMPTY
from magma.symbol_table_utils import make_master_symbol_table, MasterSymbolTable


def _make_empty(name: str):
    return (SYMBOL_TABLE_EMPTY, name)


def test_one():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {"Top": "CTop"},
            "instance_names": {("Top", "inst"): _make_empty("c_inst")},
            "port_names": {("Top", "I"): "in"},
            "inlined_instance_names": {},
            "instance_types": {("Top", "inst"): "MyModule"},
        }),
        SymbolTable.from_dict({
            "module_names": {"CTop": "VTop"},
            "instance_names": {("CTop", "c_inst"): _make_empty("v_inst")},
            "port_names": {("CTop", "in.x"): "in_x",
                           ("CTop", "in.y"): "in_y"},
            "inlined_instance_names": {},
        }),
        SymbolTable.from_dict({
            "module_names": {"VTop": "OTop"},
            "instance_names": {("VTop", "v_inst"): _make_empty("o_inst")},
            "port_names": {("VTop", "in_x"): "in_x",
                           ("VTop", "in_y"): "in_y"},
            "inlined_instance_names": {},
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "Top": "OTop"
        },
        "instance_names": {
            ("Top", "inst"): _make_empty("o_inst")
        },
        "port_names": {
            ("Top", "I.x"): "in_x",
            ("Top", "I.y"): "in_y",
        },
        "inlined_instance_names": {},
        "instance_types": {("Top", "inst"): "MyModule"},
    }


def test_two():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {"x": "y", "a": "b"},
            "instance_names": {("x", "inst0"): _make_empty("inst_0"),
                               ("a", "foo"): _make_empty("foo_out")},
            "port_names": {},
            "inlined_instance_names": {},
            "instance_types": {("x", "inst0"): "MyModule",
                               ("a", "foo"): "Foo"},
        }),
        SymbolTable.from_dict({
            "module_names": {"y": "z", "b": "b"},
            "instance_names": {("y", "inst_0"): _make_empty("inst_2"),
                               ("b", "foo_out"): _make_empty("foo_out")},
            "port_names": {},
            "inlined_instance_names": {},
        }),
        SymbolTable.from_dict({
            "module_names": {"z": "z", "b": "f"},
            "instance_names": {("z", "inst_2"): _make_empty("inst_100"),
                               ("b", "foo_out"): _make_empty("foo_OUT")},
            "port_names": {},
            "inlined_instance_names": {},
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "x": "z",
            "a": "f"
        },
        "instance_names": {
            ("x", "inst0"): _make_empty("inst_100"),
            ("a", "foo"): _make_empty("foo_OUT")
        },
        "port_names": {},
        "inlined_instance_names": {},
        "instance_types": {
            ("x", "inst0"): "MyModule",
            ("a", "foo"): "Foo"
        },
    }
