import magma
import mantle
import coreir
import os
os.environ["MANTLE"] = "coreir"

def test_compile_coreir():
    width = 16
    parallel_inputs = 4
    doubleT = magma.Bits(width)
    double = magma.DefineCircuit("double", "I", magma.In(doubleT), "O", magma.Out(doubleT))
    import math
    magma.wire(mantle.coreir.logic.static_left_shift(double.I, 2), double.O)
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

    mapNParams = c.new_values({"width": width, "parallelOperators": parallel_inputs, "operator": coreir_double})

    test_module_typ = c.Record({"in": c.Array(parallel_inputs, c.Array(width,
        c.BitIn())), "out": c.Array(parallel_inputs, c.Array(width, c.Bit()))})
    test_module = c.global_namespace.new_module("test_module", test_module_typ)
    test_module_def = test_module.new_definition()
    mapN = import_("aetherlinglib", "mapN")
    mapMod = mapN(width=width, parallelOperators=parallel_inputs, operator=coreir_double)
    mapDouble = test_module_def.add_module_instance("mapDouble", mapMod)
    test_module_def.connect(test_module_def.interface.select("in"), mapDouble.select("in"));
    test_module_def.connect(mapDouble.select("out"), test_module_def.interface.select("out"));
    test_module_def.print_()
    test_module.definition = test_module_def
    test_module.print_()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_module.save_to_file(os.path.join(dir_path, "mapN_test.json"))
    with open(os.path.join(dir_path, "mapN_test.json"), "r") as actual:
        with open(os.path.join(dir_path, "mapN_test_gold.json"), "r") as gold:
            assert actual.read() == gold.read()
    mod = c.load_from_file(os.path.join(dir_path, "mapN_test.json"))
    mod.print_()
