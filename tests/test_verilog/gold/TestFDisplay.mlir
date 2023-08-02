module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @TestFDisplay(%I: i1, %CLK: i1, %CE: i1) -> (O: i1) {
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
        %3 = hw.constant 0 : i1
        sv.verbatim "\ninteger \\_file_test_fdisplay.log ;\ninitial \\_file_test_fdisplay.log = $fopen(\"test_fdisplay.log\", \"a\");\n"
        sv.verbatim "always @(posedge {{2}}) begin\n    if ({{3}}) $fdisplay(\\_file_test_fdisplay.log , \"ff.O=%d, ff.I=%d\", {{0}}, {{1}});\nend\n" (%0, %I, %CLK, %CE) : i1, i1, i1, i1
        %4 = hw.constant 0 : i1
        sv.verbatim "\nfinal $fclose(\\_file_test_fdisplay.log );\n"
        hw.output %0 : i1
    }
}
