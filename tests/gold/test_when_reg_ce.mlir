module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_reg_ce(%I: i8, %CE: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 0 : i1
        %5 = sv.reg : !hw.inout<i8>
        %3 = sv.read_inout %5 : !hw.inout<i8>
        %6 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i8
            sv.if %CE {
                sv.bpassign %5, %I : i8
            }
        }
        %8 = sv.wire sym @test_when_reg_ce._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %8, %3 : i8
        %7 = sv.read_inout %8 : !hw.inout<i8>
        %10 = sv.wire sym @test_when_reg_ce._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %10, %4 : i1
        %9 = sv.read_inout %10 : !hw.inout<i1>
        %11 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %9 {
                sv.passign %11, %7 : i8
            }
        }
        %12 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %11, %12 : i8
        }
        %2 = sv.read_inout %11 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%CE, %7, %I) : i1, i8, i8
        %13 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%CE, %9, %13) : i1, i1, i1
        %15 = hw.constant -1 : i1
        %14 = comb.xor %15, %CE : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %7, %2) : i1, i8, i8
        hw.output %2 : i8
    }
}
