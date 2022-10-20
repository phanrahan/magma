module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @COND1_compile_guard(%port_0: i1, %CLK: i1) -> () {
        %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %port_0 : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
    }
    hw.module @COND2_compile_guard(%port_0: i1, %CLK: i1) -> () {
        %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %port_0 : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
    }
    hw.module @simple_compile_guard(%I: i1, %CLK: i1) -> (O: i1) {
        sv.ifdef "COND1" {
            hw.instance "COND1_compile_guard" @COND1_compile_guard(port_0: %I: i1, CLK: %CLK: i1) -> ()
        }
        sv.ifdef "COND2" {
        } else {
            hw.instance "COND2_compile_guard" @COND2_compile_guard(port_0: %I: i1, CLK: %CLK: i1) -> ()
        }
        hw.output %I : i1
    }
}
