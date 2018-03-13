from bit_vector import BitVector
import operator
import magma as m
import magma.testing.verilator
import delegator
import inspect
import os
from random import randint

unary_primitives = [
    ("not", operator.invert),
    # ("neg", operator.neg),
]

binary_primitives = [
    ("and", operator.and_),
    ("or", operator.or_),
    ("xor", operator.xor),
    ("add", operator.add),
    ("sub", operator.sub),
    ("mul", operator.mul),
    ("shl", operator.lshift),
    # ("lshr", operator.rshift),
]

comparison_primitives = [
    ("slt", operator.lt, True),
    ("sle", operator.le, True),
    ("sgt", operator.gt, True),
    ("sge", operator.ge, True),
    ("ult", operator.lt, False),
    ("ule", operator.le, False),
    ("ugt", operator.gt, False),
    ("uge", operator.ge, False),
]

def pytest_generate_tests(metafunc):
    if 'binary_primitive' in metafunc.fixturenames:
        metafunc.parametrize("binary_primitive", binary_primitives)
    if 'unary_primitive' in metafunc.fixturenames:
        metafunc.parametrize("unary_primitive", unary_primitives)
    if 'comparison_primitive' in metafunc.fixturenames:
        metafunc.parametrize("comparison_primitive", comparison_primitives)
    if 'width' in metafunc.fixturenames:
        metafunc.parametrize("width", [16])
    if 'input0' in metafunc.fixturenames:
        metafunc.parametrize("input0", range(16))
    if 'input1' in metafunc.fixturenames:
        metafunc.parametrize("input1", range(16))

def complete(func, n, width, signed=False):
    max = 1 << width
    tests = []
    for i in range(n):
        for j in range(n):
            test = [BitVector(i, width, signed), BitVector(j, width, signed)]
            result = func(*test)
            test.append(result)
            tests.append(test)
    return tests

def random(func, n, width, signed=False):
    max = 1 << width
    tests = []
    for i in range(n):
        x = randint(0, max)
        y = randint(0, max)
        test = [BitVector(x, width, signed), BitVector(y, width, signed)]
        result = func(*test)
        test.append(result)
        tests.append(test)
    return tests

def test_binary_primitive(binary_primitive, width):

    primitive_name, primitive_op = binary_primitive
    prim = m.DeclareCircuit(f"primitive_name",
            "in0", m.In(m.Array(width, m.Bit)),
            "in1", m.In(m.Array(width, m.Bit)),
            "out",  m.Out(m.Array(width, m.Bit)),
            coreir_lib="coreir", coreir_name=primitive_name, coreir_genargs={"width": width})
    circ = m.DefineCircuit(f"{primitive_name}_wrapper",
            "I0", m.In(m.Array(width, m.Bit)),
            "I1", m.In(m.Array(width, m.Bit)),
            "O",  m.Out(m.Array(width, m.Bit))
            )
    inst = prim()
    m.wire(circ.I0, inst.in0)
    m.wire(circ.I1, inst.in1)
    m.wire(circ.O, inst.out)
    m.EndDefine()
    m.compile(f"build/{primitive_name}", circ, output="coreir")

    file_path = os.path.dirname(__file__)
    build_dir = os.path.join(file_path, 'build')
    result = delegator.run(f"coreir -i {primitive_name}.json -o {primitive_name}.v", cwd=build_dir)
    assert not result.return_code, result.out + "\n" + result.err
    if width == 4:
        tests = complete(primitive_op, 16, width)
    else:
        assert width == 16
        tests = random(primitive_op, 512, width)
    m.testing.verilator.compile(f"build/sim_{primitive_name}.cpp", circ, tests)
    m.testing.verilator.run_verilator_test(f"{primitive_name}",
            f"sim_{primitive_name}", f"{primitive_name}_wrapper")

def test_comparison_primitive(comparison_primitive, width):

    primitive_name, primitive_op, signed = comparison_primitive
    prim = m.DeclareCircuit(f"primitive_name",
            "in0", m.In(m.Array(width, m.Bit)),
            "in1", m.In(m.Array(width, m.Bit)),
            "out",  m.Out(m.Bit),
            coreir_lib="coreir", coreir_name=primitive_name, coreir_genargs={"width": width})
    circ = m.DefineCircuit(f"{primitive_name}_wrapper",
            "I0", m.In(m.Array(width, m.Bit)),
            "I1", m.In(m.Array(width, m.Bit)),
            "O",  m.Out(m.Bit))
    inst = prim()
    m.wire(circ.I0, inst.in0)
    m.wire(circ.I1, inst.in1)
    m.wire(circ.O, inst.out)
    m.EndDefine()
    m.compile(f"build/{primitive_name}", circ, output="coreir")

    file_path = os.path.dirname(__file__)
    build_dir = os.path.join(file_path, 'build')
    result = delegator.run(f"coreir -i {primitive_name}.json -o {primitive_name}.v", cwd=build_dir)
    assert not result.return_code, result.out + "\n" + result.err
    if width == 4:
        tests = complete(primitive_op, 16, width, signed)
    else:
        assert width == 16
        tests = random(primitive_op, 512, width, signed)
    m.testing.verilator.compile(f"build/sim_{primitive_name}.cpp", circ, tests)
    m.testing.verilator.run_verilator_test(f"{primitive_name}",
            f"sim_{primitive_name}", f"{primitive_name}_wrapper")
