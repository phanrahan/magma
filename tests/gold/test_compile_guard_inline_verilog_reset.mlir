module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @WireClock(%I: i1) -> (O: i1) {
        %1 = sv.wire sym @WireClock.Wire_inst0 {name="Wire_inst0"} : !hw.inout<i1>
        sv.assign %1, %I : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        hw.output %0 : i1
    }
    hw.module @WireAsyncResetN(%I: i1) -> (O: i1) {
        %1 = sv.wire sym @WireAsyncResetN.Wire_inst0 {name="Wire_inst0"} : !hw.inout<i1>
        sv.assign %1, %I : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        hw.output %0 : i1
    }
    hw.module @COND_compile_guard(%port_0: i1, %port_1: i1, %port_2: i1) -> () {
        %1 = sv.wire sym @COND_compile_guard._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
        sv.assign %1, %port_0 : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        %2 = hw.instance "_magma_inline_wire1" @WireAsyncResetN(I: %port_1: i1) -> (O: i1)
        %3 = hw.instance "_magma_inline_wire2" @WireClock(I: %port_2: i1) -> (O: i1)
        sv.verbatim "\nassert property (@(posedge {{2}}) disable iff {{1}} {{0}} |-> ##1 {{0}};\n                " (%0, %2, %3) : i1, i1, i1
    }
    hw.module @_Top(%I: i1, %CLK: i1, %ASYNCRESETN: i1) -> (O: i1) {
        sv.ifdef "COND" {
            hw.instance "COND_compile_guard" @COND_compile_guard(port_0: %I: i1, port_1: %ASYNCRESETN: i1, port_2: %CLK: i1) -> ()
        }
        hw.output %I : i1
    }
}
