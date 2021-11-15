hw.module @complex_inline_verilog(%I: i1, %CLK: i1) -> (%O: i1) {
    %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : i1
    }
    %2 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %1, %2 : i1
    }
    %0 = sv.read_inout %1 : !hw.inout<i1>
    %4 = sv.wire sym @_magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
    sv.assign %4, %0 : i1
    %3 = sv.read_inout %4 : !hw.inout<i1>
    %6 = sv.wire sym @_magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i1>
    sv.assign %6, %I : i1
    %5 = sv.read_inout %6 : !hw.inout<i1>
    sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});" (%3, %5) : i1, i1
    hw.output %0 : i1
}
