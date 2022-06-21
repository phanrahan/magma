hw.module @complex_bind_child(%I_I: i1, %CLK: i1) -> (O_I: i1) {
    %1 = sv.reg {name = "my_reg"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I_I : i1
    }
    %2 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %1, %2 : i1
    }
    %0 = sv.read_inout %1 : !hw.inout<i1>
    hw.output %I_I : i1
}
hw.module @complex_bind_asserts(%I_I: i1, %O: i1, %CLK: i1, %I0: i1, %I1: i1, %I2: i1, %I3: i1) -> () {
    %1 = sv.wire sym @complex_bind_asserts._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
    sv.assign %1, %O : i1
    %0 = sv.read_inout %1 : !hw.inout<i1>
    %3 = sv.wire sym @complex_bind_asserts._magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i1>
    sv.assign %3, %I_I : i1
    %2 = sv.read_inout %3 : !hw.inout<i1>
    %5 = sv.wire sym @complex_bind_asserts._magma_inline_wire2 {name="_magma_inline_wire2"} : !hw.inout<i1>
    sv.assign %5, %I0 : i1
    %4 = sv.read_inout %5 : !hw.inout<i1>
    sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});assert property ({{1}} |-> {{2}};" (%0, %2, %4) : i1, i1, i1
}
hw.module @complex_bind(%I_I: i1, %CLK: i1) -> (O: i1) {
    %1 = hw.constant -1 : i1
    %0 = comb.xor %1, %I_I : i1
    %2 = comb.xor %1, %0 : i1
    %4 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %4, %2 : i1
    }
    %5 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %4, %5 : i1
    }
    %3 = sv.read_inout %4 : !hw.inout<i1>
    %6 = hw.instance "complex_bind_child_inst0" @complex_bind_child(I_I: %I_I: i1, CLK: %CLK: i1) -> (O_I: i1)
    %7 = sv.xmr "I_I" : !hw.inout<i1>
    %8 = sv.read_inout %7 : !hw.inout<i1>
    %9 = sv.xmr "complex_bind_child_inst0.O_I" : !hw.inout<i1>
    %10 = sv.read_inout %9 : !hw.inout<i1>
    %11 = sv.xmr "complex_bind_child_inst0", "my_reg", "my_reg_O_I" : !hw.inout<i1>
    %12 = sv.read_inout %11 : !hw.inout<i1>
    hw.instance "complex_bind_asserts_inst" sym @complex_bind.complex_bind_asserts_inst @complex_bind_asserts(I_I: %I_I: i1, O: %3: i1, CLK: %CLK: i1, I0: %0: i1, I1: %8: i1, I2: %10: i1, I3: %12: i1) -> () {doNotPrint = 1}
    hw.output %3 : i1
}
sv.bind #hw.innerNameRef<@complex_bind::@complex_bind.complex_bind_asserts_inst>
