module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Main(%I: i1, %arr: i2, %CLK: i1) -> (O: i1) {
        %1 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
        sv.verbatim "\nassert property (@(posedge CLK) {{1}} |-> ##1 {{0}});\n" (%0, %I) : i1, i1
        %3 = comb.extract %arr from 0 : (i2) -> i1
        %4 = comb.extract %arr from 1 : (i2) -> i1
        sv.verbatim "\nassert property (@(posedge CLK) {{0}} |-> ##1 {{1}});\n" (%3, %4) : i1, i1
        hw.output %0 : i1
    }
}
