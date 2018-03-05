import magma
import coreir
import os

def test_compile_coreir():
    width = 16
    numInputs = 4
    doubleT = magma.Bits(width)
    double = magma.DefineCircuit("double", "I", magma.In(doubleT), "O", magma.Out(doubleT))
    shift_amount = 2
    output = magma.concat(double.I[shift_amount:width], magma.bits(0, shift_amount))
    magma.wire(output, double.O)
    coreir_double = magma.backend.coreir_compile(double)
    c = coreir_double.context

    def get_lib(lib):
        if lib in {"coreir", "mantle", "corebit"}:
            return c.get_namespace(lib)
        elif lib == "global":
            return c.global_namespace
        else:
            return c.load_library(lib)

    def import_(lib, name):
        return get_lib(lib).generators[name]

    mapParallelParams = c.new_values({"numInputs": numInputs, "operator": coreir_double})

    test_module_typ = c.Record({"in": c.Array(numInputs, c.Array(width,
        c.BitIn())), "out": c.Array(numInputs, c.Array(width, c.Bit()))})
    test_module = c.global_namespace.new_module("test_module", test_module_typ)
    test_module_def = test_module.new_definition()
    mapParallel = import_("aetherlinglib", "mapParallel")
    mapMod = mapParallel(numInputs=numInputs, operator=coreir_double)
    mapDouble = test_module_def.add_module_instance("mapDouble", mapMod)
    test_module_def.connect(test_module_def.interface.select("in"), mapDouble.select("I"));
    test_module_def.connect(mapDouble.select("O"), test_module_def.interface.select("out"));
    test_module_def.print_()
    test_module.definition = test_module_def
    test_module.print_()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_module.save_to_file(os.path.join(dir_path, "mapParallel_test.json"))
    with open(os.path.join(dir_path, "mapParallel_test.json"), "r") as actual:
        with open(os.path.join(dir_path, "mapParallel_test_gold.json"), "r") as gold:
            assert actual.read() == gold.read()
    mod = c.load_from_file(os.path.join(dir_path, "mapParallel_test.json"))
    mod.print_()
