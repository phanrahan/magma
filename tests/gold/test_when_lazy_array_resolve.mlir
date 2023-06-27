module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_resolve(%I: i2, %S: i1) -> (O: i2) {
        %0 = hw.constant 1 : i2
        %1 = comb.shru %I, %0 : i2
        %2 = comb.extract %1 from 0 : (i2) -> i1
        %3 = comb.extract %1 from 1 : (i2) -> i1
        %5 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i2>
        %4 = sv.read_inout %5 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %S {
                %8 = comb.concat %7, %6 : i1, i1
                sv.bpassign %5, %8 : i2
            } else {
                %9 = comb.concat %3, %2 : i1, i1
                sv.bpassign %5, %9 : i2
            }
        }
        %6 = comb.extract %I from 0 : (i2) -> i1
        %7 = comb.extract %I from 1 : (i2) -> i1
        %10 = comb.extract %4 from 0 : (i2) -> i1
        %11 = comb.extract %I from 0 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_83: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %11) : i1, i1, i1
        %12 = comb.extract %4 from 1 : (i2) -> i1
        %13 = comb.extract %I from 1 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_84: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %13) : i1, i1, i1
        %15 = hw.constant -1 : i1
        %14 = comb.xor %15, %S : i1
        sv.verbatim "WHEN_ASSERT_85: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %10, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_86: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %12, %3) : i1, i1, i1
        hw.output %4 : i2
    }
}
