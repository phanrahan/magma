from magma import *
import magma as m

def test():
    m.config.set_debug_mode(True)
    Add = DeclareCircuit("Add", "A", In(Bit), "B", In(Bit), "C", Out(Bit))

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    add = Add()
    add(main.I0, main.I1)
    wire(add.C, main.O)
    EndCircuit()

    compile("build/dot", main, output='dot')
    m.config.set_debug_mode(False)
    # FIXME: Do equality check.
    # Let's not check for equality / check in gold until we've finalized this format.
    # assert magma_check_files_equal(__file__, "build/dot.dot", "gold/dot.dot")
