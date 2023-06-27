module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce_multiple(%I: i8, %CE: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %CE from 0 : (i2) -> i1
        %1 = hw.constant 1 : i1
        %2 = comb.extract %CE from 1 : (i2) -> i1
        %4 = hw.constant -1 : i8
        %3 = comb.xor %4, %I : i8
        %5 = hw.constant 0 : i1
        %9 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %7 = sv.read_inout %9 : !hw.inout<i8>
        %10 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %8 = sv.read_inout %10 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %6 : i8
            sv.bpassign %10, %5 : i1
            sv.if %0 {
                sv.bpassign %9, %I : i8
                sv.bpassign %10, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %9, %3 : i8
                    sv.bpassign %10, %1 : i1
                }
            }
        }
        %11 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %8 {
                sv.passign %11, %7 : i8
            }
        }
        %12 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %11, %12 : i8
        }
        %6 = sv.read_inout %11 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_149: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %7, %I) : i1, i8, i8
        %13 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_150: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %8, %13) : i1, i1, i1
        %15 = hw.constant -1 : i1
        %14 = comb.xor %15, %0 : i1
        %16 = comb.and %14, %2 : i1
        sv.verbatim "WHEN_ASSERT_151: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %7, %3) : i1, i8, i8
        %17 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_152: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %8, %17) : i1, i1, i1
        %18 = comb.or %0, %16 : i1
        %19 = comb.xor %15, %18 : i1
        sv.verbatim "WHEN_ASSERT_153: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %7, %6) : i1, i8, i8
        %20 = comb.or %0, %16 : i1
        %21 = comb.xor %15, %20 : i1
        %22 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_154: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%21, %8, %22) : i1, i1, i1
        hw.output %6 : i8
    }
}
