module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_bind_asserts(%I: i1, %O: i1, %CLK: i1) -> () {
        %1 = sv.wire sym @simple_bind_asserts._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
        sv.assign %1, %O : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        %3 = sv.wire sym @simple_bind_asserts._magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i1>
        sv.assign %3, %I : i1
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});" (%0, %2) : i1, i1
    }
    hw.module @simple_bind(%I: i1, %CLK: i1) -> (O: i1) {
        %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
        hw.instance "simple_bind_asserts_inst" sym @simple_bind.simple_bind_asserts_inst @simple_bind_asserts(I: %I: i1, O: %0: i1, CLK: %CLK: i1) -> () {doNotPrint = 1}
        hw.output %0 : i1
    }
    sv.bind #hw.innerNameRef<@simple_bind::@simple_bind.simple_bind_asserts_inst>
}
