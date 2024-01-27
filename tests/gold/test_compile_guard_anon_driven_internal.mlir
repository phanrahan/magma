module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @COND_compile_guard(in %port_0: i1) {
        %1 = sv.wire sym @COND_compile_guard.corebit_undriven_inst0 : !hw.inout<i1>
        %0 = sv.read_inout %1 : !hw.inout<i1>
        %3 = sv.wire sym @COND_compile_guard.x name "x" : !hw.inout<i1>
        sv.assign %3, %0 : i1
        %2 = sv.read_inout %3 : !hw.inout<i1>
        %5 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %port_0) {
            sv.passign %5, %2 : i1
        }
        %6 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %5, %6 : i1
        }
        %4 = sv.read_inout %5 : !hw.inout<i1>
    }
    hw.module @_Top(in %I: i1, in %CLK: i1, out O: i1) {
        sv.ifdef "COND" {
            hw.instance "COND_compile_guard" @COND_compile_guard(port_0: %CLK: i1) -> ()
        }
        hw.output %I : i1
    }
}
