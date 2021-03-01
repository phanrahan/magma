import pytest

from magma.symbol_table import SymbolTable
from magma.symbol_table_utils import make_master_symbol_table, MasterSymbolTable


def _make_master():
    #return make_master_symbol_table(("st0.json", "st1.json"))
    return MasterSymbolTable([
        # SymbolTable.from_dict({
        #     "module_names": {"Top": "CTop"},
        #     "instance_names": {("Top", "inst"): "c_inst"},
        #     "port_names": {},
        # }),
        # SymbolTable.from_dict({
        #     "module_names": {"CTop": "VTop"},
        #     "instance_names": {("CTop", "c_inst"): "v_inst"},
        #     "port_names": {},
        # }),
        # SymbolTable.from_dict({
        #     "module_names": {"VTop": "OTop"},
        #     "instance_names": {("VTop", "v_inst"): "o_inst"},
        #     "port_names": {},
        # }),
        SymbolTable.from_dict({
            "module_names": {"x": "y", "a": "b"},
            "instance_names": {("x", "inst0"): "inst_0",
                               ("a", "foo"): "foo_out"},
            "port_names": {},
        }),
        SymbolTable.from_dict({
            "module_names": {#"c": "d",
                             "y": "z"},
            "instance_names": {("y", "inst_0"): "inst_2"},
            "port_names": {},
        }),
        SymbolTable.from_dict({
            "module_names": {"b": "f"},
            "instance_names": {("b", "foo_out"): "foo_OUT",
                               ("z", "inst_2"): "inst_100"},
            "port_names": {},
        }),
    ])


def test_one():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {"Top": "CTop"},
            "instance_names": {("Top", "inst"): "c_inst"},
            "port_names": {("Top", "I"): ("", "in")},
        }),
        SymbolTable.from_dict({
            "module_names": {"CTop": "VTop"},
            "instance_names": {("CTop", "c_inst"): "v_inst"},
            "port_names": {("CTop", "in.x"): ("", "in_x"),
                           ("CTop", "in.y"): ("", "in_y")},
        }),
        SymbolTable.from_dict({
            "module_names": {"VTop": "OTop"},
            "instance_names": {("VTop", "v_inst"): "o_inst"},
            "port_names": {("VTop", "in_x"): ("", "in_x"),
                           ("VTop", "in_y"): ("", "in_y")},
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "Top": "OTop"
        },
        "instance_names": {
            ("Top", "inst"): "o_inst"
        },
        "port_names": {("Top", "I.x"): ("OTop", "in_x"),
                       ("Top", "I.y"): ("OTop", "in_y"),},
    }


def test_two():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {"x": "y", "a": "b"},
            "instance_names": {("x", "inst0"): "inst_0",
                               ("a", "foo"): "foo_out"},
            "port_names": {},
        }),
        SymbolTable.from_dict({
            "module_names": {"y": "z"},
            "instance_names": {("y", "inst_0"): "inst_2"},
            "port_names": {},
        }),
        SymbolTable.from_dict({
            "module_names": {"b": "f"},
            "instance_names": {("b", "foo_out"): "foo_OUT",
                               ("z", "inst_2"): "inst_100"},
            "port_names": {},
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "x": "z",
            "a": "f"
        },
        "instance_names": {
            ("x", "inst0"): "inst_100",
            ("a", "foo"): "foo_OUT"
        },
        "port_names": {},
    }
