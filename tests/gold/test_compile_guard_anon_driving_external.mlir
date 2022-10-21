hw.module @COND_compile_guard(%port_0: i1, %CLK: i1) -> (port_1: i1) {
    %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %port_0 : i1
    }
    %2 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %1, %2 : i1
    }
    %0 = sv.read_inout %1 : !hw.inout<i1>
    hw.output %0 : i1
}
hw.module @_Top(%I: i1, %CLK: i1) -> (O: i1) {
    sv.ifdef "COND" {
        %0 = hw.instance "COND_compile_guard" @COND_compile_guard(port_0: %I: i1, CLK: %CLK: i1) -> (port_1: i1)
    }
    %2 = sv.wire sym @_Top.x {name="x"} : !hw.inout<i1>
    sv.assign %2, %0 : i1
    %1 = sv.read_inout %2 : !hw.inout<i1>
    hw.output %1 : i1
}
