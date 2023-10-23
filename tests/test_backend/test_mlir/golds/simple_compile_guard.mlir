module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @COND1_compile_guard(%port_0: i1, %port_1: i1) -> () {
        %1 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %port_1) {
            sv.passign %1, %port_0 : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
    }
    hw.module @COND2_compile_guard(%port_0: i1, %port_1: i1) -> () {
        %1 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %port_1) {
            sv.passign %1, %port_0 : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
    }
    hw.module @simple_compile_guard(%I: i1, %CLK: i1) -> (O: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
        %2 = hw.constant 0 : i1
        %4 = sv.reg : !hw.inout<i1>
        sv.ifdef "COND1" {
            sv.assign %4, %I : i1
        } else {
            sv.ifdef "COND2" {
                sv.assign %4, %0 : i1
            } else {
                sv.assign %4, %2 : i1
            }
        }
        %3 = sv.read_inout %4 : !hw.inout<i1>
        sv.ifdef "COND1" {
            hw.instance "COND1_compile_guard" @COND1_compile_guard(port_0: %I: i1, port_1: %CLK: i1) -> ()
        }
        sv.ifdef "COND2" {
        } else {
            hw.instance "COND2_compile_guard" @COND2_compile_guard(port_0: %I: i1, port_1: %CLK: i1) -> ()
        }
        hw.output %3 : i1
    }
}
