module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array(%S: i1) -> (O: i2) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 1 : i1
        %4 = sv.reg name "_WHEN_WIRE_61" : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg name "_WHEN_WIRE_62" : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %4, %0 : i1
                sv.bpassign %5, %1 : i1
            } else {
                sv.bpassign %4, %1 : i1
                sv.bpassign %5, %0 : i1
            }
        }
        %6 = comb.concat %3, %2 : i1, i1
        %8 = sv.wire sym @test_when_lazy_array.x name "x" : !hw.inout<i2>
        sv.assign %8, %6 : i2
        %7 = sv.read_inout %8 : !hw.inout<i2>
        %9 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_69: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %2, %9) : i1, i1, i1
        %10 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_70: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %3, %10) : i1, i1, i1
        %12 = hw.constant -1 : i1
        %11 = comb.xor %12, %S : i1
        %13 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_71: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %2, %13) : i1, i1, i1
        %14 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_72: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %3, %14) : i1, i1, i1
        hw.output %7 : i2
    }
}
