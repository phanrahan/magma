module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_double_elsewhen(in %I: i2, in %S: i2, out O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %3 = comb.extract %I from 1 : (i2) -> i1
        %5 = hw.constant -1 : i2
        %4 = comb.icmp eq %S, %5 : i2
        %6 = hw.constant 1 : i1
        %8 = sv.reg : !hw.inout<i1>
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
        %10 = sv.wire sym @test_when_double_elsewhen._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %10, %7 : i1
        %9 = sv.read_inout %10 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %9, %1) : i1, i1, i1
        %12 = hw.constant -1 : i1
        %11 = comb.xor %12, %0 : i1
        %13 = comb.and %11, %2 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%13, %9, %3) : i1, i1, i1
        %14 = comb.xor %12, %2 : i1
        %15 = comb.and %11, %14 : i1
        %16 = comb.and %15, %4 : i1
        %17 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %9, %17) : i1, i1, i1
        %18 = comb.xor %12, %4 : i1
        %19 = comb.and %15, %18 : i1
        %20 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %9, %20) : i1, i1, i1
        hw.output %9 : i1
    }
}
