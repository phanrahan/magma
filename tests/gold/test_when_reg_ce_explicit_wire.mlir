module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_reg_ce_explicit_wire(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 0 : i1
        %4 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %4, %1 : i8
            sv.bpassign %5, %0 : i1
            sv.if %y {
                sv.bpassign %4, %I : i8
                sv.bpassign %5, %x : i1
            }
        }
        %7 = sv.wire sym @test_when_reg_ce_explicit_wire._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %7, %2 : i8
        %6 = sv.read_inout %7 : !hw.inout<i8>
        %9 = sv.wire sym @test_when_reg_ce_explicit_wire._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %9, %3 : i1
        %8 = sv.read_inout %9 : !hw.inout<i1>
        %10 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %8 {
                sv.passign %10, %6 : i8
            }
        }
        %11 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %10, %11 : i8
        }
        %1 = sv.read_inout %10 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %6, %I) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %8, %x) : i1, i1, i1
        %13 = hw.constant -1 : i1
        %12 = comb.xor %13, %y : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%12, %6, %1) : i1, i8, i8
        %14 = comb.xor %13, %y : i1
        %15 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %8, %15) : i1, i1, i1
        hw.output %1 : i8
    }
}
