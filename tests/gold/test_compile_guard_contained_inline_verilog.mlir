module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @DebugModule(%port_0: i1, %port_1: i1, %port_2: i1) -> () {
        %1 = comb.or %0, %port_1 : i1
        %2 = sv.reg name "reg" : !hw.inout<i1>
        sv.alwaysff(posedge %port_0) {
            sv.passign %2, %1 : i1
        }
        %3 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %2, %3 : i1
        }
        %0 = sv.read_inout %2 : !hw.inout<i1>
        sv.verbatim "assert {{0}};" (%port_2) : i1
        sv.verbatim "assert ~{{0}};" (%0) : i1
    }
    hw.module @Top(%I: i1, %CLK: i1) -> (O: i1) {
        sv.ifdef "DEBUG" {
            hw.instance "DebugModule" @DebugModule(port_0: %CLK: i1, port_1: %I: i1, port_2: %I: i1) -> ()
        }
        hw.output %I : i1
    }
}
