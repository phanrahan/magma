hw.module @simple_compile_guard2(%I: i1, %CLK: i1) -> (O: i1) {
    sv.ifdef "COND1" {
        %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i1
        }
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
    }
    %2 = hw.constant 0 : i1
    sv.ifdef "COND2" {
    } else {
        %4 = sv.reg {name = "Register_inst1"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %4, %I : i1
        }
        sv.initial {
            sv.bpassign %4, %2 : i1
        }
        %3 = sv.read_inout %4 : !hw.inout<i1>
    }
    hw.output %I : i1
}
