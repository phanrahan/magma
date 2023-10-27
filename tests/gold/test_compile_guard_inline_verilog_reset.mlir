module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @COND_compile_guard(in %port_0: i1, in %port_1: i1, in %port_2: i1) {
        sv.verbatim "\nassert property (@(posedge {{2}}) disable iff {{1}} {{0}} |-> ##1 {{0}};\n                " (%port_0, %port_1, %port_2) : i1, i1, i1
    }
    hw.module @_Top(in %I: i1, in %CLK: i1, in %ASYNCRESETN: i1, out O: i1) {
        sv.ifdef "COND" {
            hw.instance "COND_compile_guard" @COND_compile_guard(port_0: %I: i1, port_1: %ASYNCRESETN: i1, port_2: %CLK: i1) -> ()
        }
        hw.output %I : i1
    }
}
