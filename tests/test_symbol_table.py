import pytest
import random
import string

from magma.symbol_table import SymbolTable


_NUM_TRIALS = 100
_NAME_SIZE = 10


def _random_name(size):
    return ''.join(random.choice(string.ascii_letters) for _ in range(size))


def _check_equal(l, r):
    if isinstance(l, tuple) and not isinstance(r, tuple):
        r = (r,)
    elif isinstance(r, tuple) and not isinstance(l, tuple):
        l = (l,)
    return l == r


def _test_basic_mapping(setter, getter, in_size, out_size, num_trials):
    golden = {}
    for i in range(num_trials):
        ins = tuple(_random_name(_NAME_SIZE) for _ in range(in_size))
        outs = tuple(_random_name(_NAME_SIZE) for _ in range(out_size))
        expect_error = ins in golden
        if not expect_error:
            setter(*(ins + outs))
            _check_equal(getter(*ins), outs)
            continue
        with pytest.raises(KeyError) as pytest_e:
            setter(*ins)
            assert False
        assert pytest_e.type is KeyError


def test_module_name():
    table = SymbolTable()

    def _setter(*args):
        table.set_module_name(*args)

    def _getter(*args):
        return table.get_module_name(*args)

    _test_basic_mapping(_setter, _getter, 1, 1, _NUM_TRIALS)


def test_instance_name():
    table = SymbolTable()

    def _setter(*args):
        table.set_instance_name(*args)

    def _getter(*args):
        return table.get_instance_name(*args)

    _test_basic_mapping(_setter, _getter, 2, 1, _NUM_TRIALS)


def test_port_name():
    table = SymbolTable()

    def _setter(*args):
        table.set_port_name(*args)

    def _getter(*args):
        return table.get_port_name(*args)

    _test_basic_mapping(_setter, _getter, 2, 2, _NUM_TRIALS)


def test_json():
    EXPECTED_JSON = ('{"module_names": {"Foo": "vFoo"}, '
                     '"instance_names": {"Foo,bar": "vbar"}, '
                     '"port_names": {"Foo,I": ["vFoo", "vI"]}}')

    table = SymbolTable()
    table.set_module_name("Foo", "vFoo")
    table.set_instance_name("Foo", "bar", "vbar")
    table.set_port_name("Foo", "I", "vFoo", "vI")

    as_json = table.as_json()
    assert as_json == EXPECTED_JSON

    copy = SymbolTable.from_json(as_json)
    assert table.get_module_name("Foo") == "vFoo"
    assert table.get_instance_name("Foo", "bar") == "vbar"
    assert table.get_port_name("Foo", "I") == ("vFoo", "vI")
    assert copy.as_json() == EXPECTED_JSON
