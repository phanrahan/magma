module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @TestDisplay(%I: i1, %CLK: i1, %CE: i1) -> (O: i1) {
        %1 = sv.reg name "ff" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.if %CE {
                sv.passign %1, %I : i1
            }
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
        sv.verbatim "always @(posedge {{2}}) begin\n    if ({{3}}) $display(\"%0t: ff.O=%d, ff.I=%d\", $time, {{0}}, {{1}});\nend\n" (%0, %I, %CLK, %CE) : i1, i1, i1, i1
        hw.output %0 : i1
    }
}
