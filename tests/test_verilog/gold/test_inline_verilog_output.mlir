module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Main(%I: i1, %arr: i2, %CLK: i1) -> (O: i1) {
        %1 = sv.reg : !hw.inout<i1>
        %0 = sv.read_inout %1 : !hw.inout<i1>
        sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});" (%0, %I) : i1, i1
        hw.output %0 : i1
    }
}
