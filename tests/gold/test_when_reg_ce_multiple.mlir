module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_reg_ce_multiple(in %I: i8, in %CE: i2, in %CLK: i1, out O: i8) {
        %0 = comb.extract %CE from 0 : (i2) -> i1
        %1 = hw.constant 1 : i1
        %2 = comb.extract %CE from 1 : (i2) -> i1
        %4 = hw.constant -1 : i8
        %3 = comb.xor %4, %I : i8
        %5 = hw.constant 0 : i1
        %9 = sv.reg : !hw.inout<i8>
        %7 = sv.read_inout %9 : !hw.inout<i8>
        %10 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %10 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %6 : i8
            sv.if %0 {
                sv.bpassign %9, %I : i8
            } else {
                sv.if %2 {
                    sv.bpassign %9, %3 : i8
                }
            }
        }
        %12 = sv.wire sym @test_when_reg_ce_multiple._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %12, %7 : i8
        %11 = sv.read_inout %12 : !hw.inout<i8>
        %14 = sv.wire sym @test_when_reg_ce_multiple._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %14, %8 : i1
        %13 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %13 {
                sv.passign %15, %11 : i8
            }
        }
        %16 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %15, %16 : i8
        }
        %6 = sv.read_inout %15 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %11, %I) : i1, i8, i8
        %17 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %13, %17) : i1, i1, i1
        %19 = hw.constant -1 : i1
        %18 = comb.xor %19, %0 : i1
        %20 = comb.and %18, %2 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %11, %3) : i1, i8, i8
        %21 = comb.or %0, %20 : i1
        %22 = comb.xor %19, %21 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%22, %11, %6) : i1, i8, i8
        hw.output %6 : i8
    }
}
