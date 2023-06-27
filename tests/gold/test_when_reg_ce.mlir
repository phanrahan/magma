module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce(%I: i8, %CE: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 0 : i1
        %5 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %3 = sv.read_inout %5 : !hw.inout<i8>
        %6 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i8
            sv.bpassign %6, %1 : i1
            sv.if %CE {
                sv.bpassign %5, %I : i8
                sv.bpassign %6, %0 : i1
            }
        }
        %7 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %4 {
                sv.passign %7, %3 : i8
            }
        }
        %8 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %7, %8 : i8
        }
        %2 = sv.read_inout %7 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_145: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%CE, %3, %I) : i1, i8, i8
        %9 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_146: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%CE, %4, %9) : i1, i1, i1
        %11 = hw.constant -1 : i1
        %10 = comb.xor %11, %CE : i1
        sv.verbatim "WHEN_ASSERT_147: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%10, %3, %2) : i1, i8, i8
        %12 = comb.xor %11, %CE : i1
        %13 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_148: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%12, %4, %13) : i1, i1, i1
        hw.output %2 : i8
    }
}
