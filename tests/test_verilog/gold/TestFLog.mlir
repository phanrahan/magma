module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @TestFLog(%I: i1, %CLK: i1, %CE: i1) -> (O: i1) {
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
        sv.verbatim "\n`ifndef MAGMA_LOG_LEVEL\n    `define MAGMA_LOG_LEVEL 1\n`endif" (%3) : i1
        %4 = hw.constant 0 : i1
        sv.verbatim "\ninteger \\_file_test_flog.log ;\ninitial \\_file_test_flog.log = $fopen(\"test_flog.log\", \"a\");\n" (%4) : i1
        sv.verbatim "always @(posedge {{2}}) begin\n    if ((`MAGMA_LOG_LEVEL <= 0) && ({{3}})) $fdisplay(\\_file_test_flog.log , \"[DEBUG] ff.O=%d, ff.I=%d\", {{0}}, {{1}});\nend\n" (%0, %I, %CLK, %CE) : i1, i1, i1, i1
        sv.verbatim "always @(posedge {{2}}) begin\n    if ((`MAGMA_LOG_LEVEL <= 1) && ({{3}})) $fdisplay(\\_file_test_flog.log , \"[INFO] ff.O=%d, ff.I=%d\", {{0}}, {{1}});\nend\n" (%0, %I, %CLK, %CE) : i1, i1, i1, i1
        sv.verbatim "always @(posedge {{2}}) begin\n    if ((`MAGMA_LOG_LEVEL <= 2) && ({{3}})) $fdisplay(\\_file_test_flog.log , \"[WARNING] ff.O=%d, ff.I=%d\", {{0}}, {{1}});\nend\n" (%0, %I, %CLK, %CE) : i1, i1, i1, i1
        sv.verbatim "always @(posedge {{2}}) begin\n    if ((`MAGMA_LOG_LEVEL <= 3) && ({{3}})) $fdisplay(\\_file_test_flog.log , \"[ERROR] ff.O=%d, ff.I=%d\", {{0}}, {{1}});\nend\n" (%0, %I, %CLK, %CE) : i1, i1, i1, i1
        %5 = hw.constant 0 : i1
        sv.verbatim "\nfinal $fclose(\\_file_test_flog.log );\n" (%5) : i1
        hw.output %0 : i1
    }
}
