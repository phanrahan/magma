import pytest
from typing import Optional

from magma.symbol_table import (SymbolTable, SYMBOL_TABLE_EMPTY,
                                SYMBOL_TABLE_INLINED_INSTANCE)
from magma.symbol_table_utils import (make_master_symbol_table, MasterSymbolTable,
                                      SymbolQueryInterface)


def _make_empty(name: str):
    return (SYMBOL_TABLE_EMPTY, name)


def _make_inlined(key: Optional[str] = None):
    name = "" if key is None else key
    return (SYMBOL_TABLE_INLINED_INSTANCE, name)


def test_one():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {
                "Top": "CTop",
                "MyModule": "MyModule",
            },
            "instance_names": {
                ("Top", "inst"): _make_empty("c_inst"),
            },
            "port_names": {
                ("Top", "I"): "in",
            },
            "instance_types": {
                ("Top", "inst"): "MyModule",
            },
        }),
        SymbolTable.from_dict({
            "module_names": {
                "CTop": "VTop",
                "MyModule": "MyModule",
            },
            "instance_names": {
                ("CTop", "c_inst"): _make_empty("v_inst"),
            },
            "port_names": {
                ("CTop", "in.x"): "in_x",
                ("CTop", "in.y"): "in_y",
            },
        }),
        SymbolTable.from_dict({
            "module_names": {
                "VTop": "OTop",
                "MyModule": "MyModule",
            },
            "instance_names": {
                ("VTop", "v_inst"): _make_empty("o_inst"),
            },
            "port_names": {
                ("VTop", "in_x"): "in_x",
                ("VTop", "in_y"): "in_y",
            },
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "Top": "OTop",
            "MyModule": "MyModule",
        },
        "instance_names": {
            ("Top", "inst"): _make_empty("o_inst"),
        },
        "port_names": {
            ("Top", "I.x"): "in_x",
            ("Top", "I.y"): "in_y",
        },
        "inlined_instance_names": {},
        "instance_types": {
            ("Top", "inst"): "MyModule",
        },
    }
    tli = SymbolQueryInterface(master)
    assert tli.get_module_name("Top") == "OTop"
    assert tli.get_instance_name("Top.inst") == "OTop.o_inst"


def test_two():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {
                "x": "y",
                "a": "b",
                "MyModule": "MyModule",
                "Foo": "Foo",
            },
            "instance_names": {
                ("x", "inst0"): _make_empty("inst_0"),
                ("a", "foo"): _make_empty("foo_out"),
            },
            "instance_types": {
                ("x", "inst0"): "MyModule",
                ("a", "foo"): "Foo",
            },
        }),
        SymbolTable.from_dict({
            "module_names": {
                "y": "z",
                "b": "b",
                "MyModule": "MyModule",
                "Foo": "Foo",
            },
            "instance_names": {
                ("y", "inst_0"): _make_empty("inst_2"),
                ("b", "foo_out"): _make_empty("foo_out"),
            },
        }),
        SymbolTable.from_dict({
            "module_names": {
                "z": "z",
                "b": "f",
                "MyModule": "MyModule",
                "Foo": "Foo",
            },
            "instance_names": {
                ("z", "inst_2"): _make_empty("inst_100"),
                ("b", "foo_out"): _make_empty("foo_OUT"),
            },
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "x": "z",
            "a": "f",
            "MyModule": "MyModule",
            "Foo": "Foo",
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


def test_inlining_simple():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {
                "M1": "M1",
                "M2": "M2",
                "M3": "M3",
            },
            "instance_names": {
                ("M1", "i2"): _make_empty("i2"),
                ("M2", "i3"): _make_empty("i3"),
            },
            "instance_types": {
                ("M1", "i2"): "M2",
                ("M2", "i3"): "M3",
            },
        }),
        SymbolTable.from_dict({
            "module_names": {
                "M1": "M1",
                "M2": "M2",
                "M3": "M3",
            },
            "instance_names": {
                ("M1", "i2"): _make_inlined(),
                ("M2", "i3"): _make_empty("i3"),
            },
            "inlined_instance_names": {
                ("M1", "i2", "i3"): _make_empty("i2$i3"),
            },
            "instance_types": {
                ("M1", "i2"): "M2",
                ("M2", "i3"): "M3",
            },
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "M1": "M1",
            "M2": "M2",
            "M3": "M3",
        },
        "instance_names": {
            ("M1", "i2"): _make_inlined(),
            ("M2", "i3"): _make_empty("i3"),
        },
        "port_names": {},
        "inlined_instance_names": {
            ("M1", "i2", "i3"): _make_empty("i2$i3"),
        },
        "instance_types": {
            ("M1", "i2"): "M2",
            ("M2", "i3"): "M3",
        },
    }
    tli = SymbolQueryInterface(master)
    assert tli.get_instance_name("M1.i2.i3") == "M1.i2$i3"
    with pytest.raises(SymbolQueryInterface.InlinedLeafInstanceError):
        tli.get_instance_name("M1.i2")


def test_inlining_top_down():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {
                "M1": "M1",
                "M2": "M2",
                "M3": "M3",
                "M4": "M4",
                "M5": "M5",
                "M6": "M6",
            },
            "instance_names": {
                ("M1", "i2"): _make_empty("i2"),
                ("M2", "i3"): _make_empty("i3"),
                ("M3", "i4"): _make_empty("i4"),
                ("M4", "i5"): _make_empty("i5"),
                ("M5", "i6"): _make_empty("i6"),
            },
            "instance_types": {
                ("M1", "i2"): "M2",
                ("M2", "i3"): "M3",
                ("M3", "i4"): "M4",
                ("M4", "i5"): "M5",
                ("M5", "i6"): "M6",
            },
        }),
        SymbolTable.from_dict({
            "module_names": {
                "M1": "M1",
                "M2": "M2",
                "M3": "M3",
                "M4": "M4",
                "M5": "M5",
                "M6": "M6",
            },
            "instance_names": {
                ("M1", "i2"): _make_inlined(),
                ("M2", "i3"): _make_empty("i3"),
                ("M3", "i4"): _make_empty("i4"),
                ("M4", "i5"): _make_empty("i5"),
                ("M5", "i6"): _make_empty("i6"),
            },
            "inlined_instance_names": {
                ("M1", "i2", "i3"): _make_inlined("UNIQ_KEY_0"),
                ("M1", "UNIQ_KEY_0", "i4"): _make_empty("i2$i3$i4"),
            },
            "instance_types": {
                ("M1", "i2"): "M2",
                ("M2", "i3"): "M3",
                ("M3", "i4"): "M4",
                ("M4", "i5"): "M5",
                ("M5", "i6"): "M6",
            },
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "M1": "M1",
            "M2": "M2",
            "M3": "M3",
            "M4": "M4",
            "M5": "M5",
            "M6": "M6",
        },
        "instance_names": {
            ("M1", "i2"): _make_inlined(),
            ("M2", "i3"): _make_empty("i3"),
            ("M3", "i4"): _make_empty("i4"),
            ("M4", "i5"): _make_empty("i5"),
            ("M5", "i6"): _make_empty("i6"),
        },
        "port_names": {},
        "inlined_instance_names": {
            ("M1", "i2", "i3"): _make_inlined("UNIQ_KEY_0"),
            ("M1", "UNIQ_KEY_0", "i4"): _make_empty("i2$i3$i4"),
        },
        "instance_types": {
            ("M1", "i2"): "M2",
            ("M2", "i3"): "M3",
            ("M3", "i4"): "M4",
            ("M4", "i5"): "M5",
            ("M5", "i6"): "M6",
        },
    }
    tli = SymbolQueryInterface(master)
    with pytest.raises(SymbolQueryInterface.InlinedLeafInstanceError):
        tli.get_instance_name("M1.i2")
    with pytest.raises(SymbolQueryInterface.InlinedLeafInstanceError):
        tli.get_instance_name("M1.i2.i3")
    assert tli.get_instance_name("M1.i2.i3.i4") == "M1.i2$i3$i4"
    assert tli.get_instance_name("M1.i2.i3.i4.i5.i6") == "M1.i2$i3$i4.i5.i6"
    assert tli.get_instance_name("M2.i3") == "M2.i3"
    assert tli.get_instance_name("M2.i3.i4") == "M2.i3.i4"


def test_inlining_bottom_up():
    master = MasterSymbolTable([
        SymbolTable.from_dict({
            "module_names": {
                "M1": "M1",
                "M2": "M2",
                "M3": "M3",
                "M4": "M4",
                "M5": "M5",
                "M6": "M6",
            },
            "instance_names": {
                ("M1", "i2"): _make_empty("i2"),
                ("M2", "i3"): _make_empty("i3"),
                ("M3", "i4"): _make_empty("i4"),
                ("M4", "i5"): _make_empty("i5"),
                ("M5", "i6"): _make_empty("i6"),
            },
            "port_names": {},
            "inlined_instance_names": {},
            "instance_types": {
                ("M1", "i2"): "M2",
                ("M2", "i3"): "M3",
                ("M3", "i4"): "M4",
                ("M4", "i5"): "M5",
                ("M5", "i6"): "M6",
            },
        }),
        SymbolTable.from_dict({
            "module_names": {
                "M1": "M1",
                "M2": "M2",
                "M3": "M3",
                "M4": "M4",
                "M5": "M5",
                "M6": "M6",
            },
            "instance_names": {
                ("M1", "i2"): _make_inlined(),
                ("M2", "i3"): _make_inlined(),
                ("M3", "i4"): _make_empty("i4"),
                ("M4", "i5"): _make_empty("i5"),
                ("M5", "i6"): _make_empty("i6"),
            },
            "port_names": {},
            "inlined_instance_names": {
                ("M1", "i2", "i3"): _make_inlined("UNIQ_KEY_0"),
                ("M1", "UNIQ_KEY_0", "i4"): _make_empty("i2$i3$i4"),
                ("M2", "i3", "i4"): _make_empty("i3$i4"),
            },
            "instance_types": {
                ("M1", "i2"): "M2",
                ("M2", "i3"): "M3",
                ("M3", "i4"): "M4",
                ("M4", "i5"): "M5",
                ("M5", "i6"): "M6",
            },
        }),
    ])
    dct = master.as_dict()
    assert dct == {
        "module_names": {
            "M1": "M1",
            "M2": "M2",
            "M3": "M3",
            "M4": "M4",
            "M5": "M5",
            "M6": "M6",
        },
        "instance_names": {
            ("M1", "i2"): _make_inlined(),
            ("M2", "i3"): _make_inlined(),
            ("M3", "i4"): _make_empty("i4"),
            ("M4", "i5"): _make_empty("i5"),
            ("M5", "i6"): _make_empty("i6"),
        },
        "port_names": {},
        "inlined_instance_names": {
            ("M1", "i2", "i3"): _make_inlined("UNIQ_KEY_0"),
            ("M1", "UNIQ_KEY_0", "i4"): _make_empty("i2$i3$i4"),
            ("M2", "i3", "i4"): _make_empty("i3$i4"),
        },
        "instance_types": {
            ("M1", "i2"): "M2",
            ("M2", "i3"): "M3",
            ("M3", "i4"): "M4",
            ("M4", "i5"): "M5",
            ("M5", "i6"): "M6",
        },
    }
    tli = SymbolQueryInterface(master)
    with pytest.raises(SymbolQueryInterface.InlinedLeafInstanceError):
        tli.get_instance_name("M1.i2")
    with pytest.raises(SymbolQueryInterface.InlinedLeafInstanceError):
        tli.get_instance_name("M1.i2.i3")
    assert tli.get_instance_name("M1.i2.i3.i4") == "M1.i2$i3$i4"
    assert tli.get_instance_name("M1.i2.i3.i4.i5.i6") == "M1.i2$i3$i4.i5.i6"
    with pytest.raises(SymbolQueryInterface.InlinedLeafInstanceError):
        tli.get_instance_name("M2.i3")
    assert tli.get_instance_name("M2.i3.i4") == "M2.i3$i4"
    assert tli.get_instance_name("M2.i3.i4.i5") == "M2.i3$i4.i5"
