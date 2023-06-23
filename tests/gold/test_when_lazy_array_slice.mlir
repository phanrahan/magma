module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice(%S: i1) -> (O: i4) {
        %0 = hw.constant 0 : i2
        %1 = hw.constant 1 : i2
        %2 = hw.constant 1 : i2
        %3 = hw.constant 0 : i2
        %4 = hw.constant 0 : i1
        %5 = hw.constant 1 : i1
        %12 = sv.reg name "_WHEN_WIRE_63" : !hw.inout<i2>
        %6 = sv.read_inout %12 : !hw.inout<i2>
        %13 = sv.reg name "_WHEN_WIRE_64" : !hw.inout<i2>
        %7 = sv.read_inout %13 : !hw.inout<i2>
        %14 = sv.reg name "_WHEN_WIRE_65" : !hw.inout<i1>
        %8 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg name "_WHEN_WIRE_66" : !hw.inout<i1>
        %9 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg name "_WHEN_WIRE_67" : !hw.inout<i1>
        %10 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg name "_WHEN_WIRE_68" : !hw.inout<i1>
        %11 = sv.read_inout %17 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %14, %4 : i1
                sv.bpassign %15, %4 : i1
                sv.bpassign %16, %5 : i1
                sv.bpassign %17, %4 : i1
            } else {
                sv.bpassign %14, %5 : i1
                sv.bpassign %15, %4 : i1
                sv.bpassign %16, %4 : i1
                sv.bpassign %17, %4 : i1
            }
        }
        %18 = comb.concat %11, %10, %9, %8 : i1, i1, i1, i1
        %20 = sv.wire sym @test_when_lazy_array_slice.x name "x" : !hw.inout<i4>
        sv.assign %20, %18 : i4
        %19 = sv.read_inout %20 : !hw.inout<i4>
        %21 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_73: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %8, %21) : i1, i1, i1
        %22 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_74: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %9, %22) : i1, i1, i1
        %23 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_75: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %23) : i1, i1, i1
        %24 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_76: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %11, %24) : i1, i1, i1
        %26 = hw.constant -1 : i1
        %25 = comb.xor %26, %S : i1
        %27 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_77: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %8, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_78: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %9, %28) : i1, i1, i1
        %29 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_79: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %10, %29) : i1, i1, i1
        %30 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_80: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %11, %30) : i1, i1, i1
        hw.output %19 : i4
    }
}
