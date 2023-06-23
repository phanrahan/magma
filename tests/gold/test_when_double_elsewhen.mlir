module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_double_elsewhen(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %3 = comb.extract %I from 1 : (i2) -> i1
        %5 = hw.constant -1 : i2
        %4 = comb.icmp eq %S, %5 : i2
        %6 = hw.constant 1 : i1
        %8 = sv.reg name "_WHEN_WIRE_58" : !hw.inout<i1>
        %7 = sv.read_inout %8 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %8, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %8, %3 : i1
                } else {
                    sv.if %4 {
                        sv.bpassign %8, %6 : i1
                    } else {
                        sv.bpassign %8, %6 : i1
                    }
                }
            }
        }
        sv.verbatim "WHEN_ASSERT_58: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %7, %1) : i1, i1, i1
        %10 = hw.constant -1 : i1
        %9 = comb.xor %10, %0 : i1
        %11 = comb.and %9, %2 : i1
        sv.verbatim "WHEN_ASSERT_59: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %7, %3) : i1, i1, i1
        %12 = comb.xor %10, %2 : i1
        %13 = comb.and %9, %12 : i1
        %14 = comb.and %13, %4 : i1
        %15 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_60: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %7, %15) : i1, i1, i1
        %16 = comb.xor %10, %4 : i1
        %17 = comb.and %13, %16 : i1
        %18 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_61: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%17, %7, %18) : i1, i1, i1
        hw.output %7 : i1
    }
}
