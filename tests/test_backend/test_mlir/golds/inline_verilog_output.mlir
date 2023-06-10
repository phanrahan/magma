module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @inline_verilog_output(%I: i1, %CLK: i1) -> (O: i1) {
        %1 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
        sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});" (%0, %I) : i1, i1
        hw.output %0 : i1
    }
}