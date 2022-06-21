hw.module @complex_bind_child(%I: !hw.struct<I: i1>, %CLK: i1) -> (O: !hw.struct<I: i1>) {
    %1 = sv.reg {name = "my_reg"} : !hw.inout<!hw.struct<I: i1>>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : !hw.struct<I: i1>
    }
    %3 = hw.constant 0 : i1
    %2 = hw.struct_create (%3) : !hw.struct<I: i1>
    sv.initial {
        sv.bpassign %1, %2 : !hw.struct<I: i1>
    }
    %0 = sv.read_inout %1 : !hw.inout<!hw.struct<I: i1>>
    hw.output %I : !hw.struct<I: i1>
}
hw.module @complex_bind_asserts(%I: !hw.struct<I: i1>, %O: i1, %CLK: i1, %I0: i1, %I1: i1, %I2: i1, %I3: i1) -> () {
    %1 = sv.wire sym @complex_bind_asserts._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
    sv.assign %1, %O : i1
    %0 = sv.read_inout %1 : !hw.inout<i1>
    %2 = hw.struct_extract %I["I"] : !hw.struct<I: i1>
    %4 = sv.wire sym @complex_bind_asserts._magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i1>
    sv.assign %4, %2 : i1
    %3 = sv.read_inout %4 : !hw.inout<i1>
    %6 = sv.wire sym @complex_bind_asserts._magma_inline_wire2 {name="_magma_inline_wire2"} : !hw.inout<i1>
    sv.assign %6, %I0 : i1
    %5 = sv.read_inout %6 : !hw.inout<i1>
    sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});assert property ({{1}} |-> {{2}};" (%0, %3, %5) : i1, i1, i1
}
hw.module @complex_bind(%I: !hw.struct<I: i1>, %CLK: i1) -> (O: i1) {
    %0 = hw.struct_extract %I["I"] : !hw.struct<I: i1>
    %2 = hw.constant -1 : i1
    %1 = comb.xor %2, %0 : i1
    %3 = comb.xor %2, %1 : i1
    %5 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %5, %3 : i1
    }
    %6 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %5, %6 : i1
    }
    %4 = sv.read_inout %5 : !hw.inout<i1>
    %7 = hw.instance "complex_bind_child_inst0" @complex_bind_child(I: %I: !hw.struct<I: i1>, CLK: %CLK: i1) -> (O: !hw.struct<I: i1>)
    %8 = sv.xmr "I.I" : !hw.inout<i1>
    %9 = sv.read_inout %8 : !hw.inout<i1>
    %10 = sv.xmr "complex_bind_child_inst0.O.I" : !hw.inout<i1>
    %11 = sv.read_inout %10 : !hw.inout<i1>
    %12 = sv.xmr "complex_bind_child_inst0", "my_reg", "my_reg", "O", "I" : !hw.inout<i1>
    %13 = sv.read_inout %12 : !hw.inout<i1>
    hw.instance "complex_bind_asserts_inst" sym @complex_bind.complex_bind_asserts_inst @complex_bind_asserts(I: %I: !hw.struct<I: i1>, O: %4: i1, CLK: %CLK: i1, I0: %1: i1, I1: %9: i1, I2: %11: i1, I3: %13: i1) -> () {doNotPrint = 1}
    hw.output %4 : i1
}
sv.bind #hw.innerNameRef<@complex_bind::@complex_bind.complex_bind_asserts_inst>
