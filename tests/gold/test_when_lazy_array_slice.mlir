module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_lazy_array_slice(%S: i1) -> (O: i4) {
        %0 = hw.constant 0 : i2
        %1 = hw.constant 1 : i2
        %2 = hw.constant 1 : i2
        %3 = hw.constant 0 : i2
        %4 = hw.constant 0 : i1
        %5 = hw.constant 1 : i1
        %12 = sv.reg : !hw.inout<i2>
        %6 = sv.read_inout %12 : !hw.inout<i2>
        %13 = sv.reg : !hw.inout<i2>
        %7 = sv.read_inout %13 : !hw.inout<i2>
        %14 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i1>
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
        %19 = sv.wire sym @test_when_lazy_array_slice._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %19, %8 : i1
        %18 = sv.read_inout %19 : !hw.inout<i1>
        %21 = sv.wire sym @test_when_lazy_array_slice._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %21, %9 : i1
        %20 = sv.read_inout %21 : !hw.inout<i1>
        %23 = sv.wire sym @test_when_lazy_array_slice._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %23, %10 : i1
        %22 = sv.read_inout %23 : !hw.inout<i1>
        %25 = sv.wire sym @test_when_lazy_array_slice._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %25, %11 : i1
        %24 = sv.read_inout %25 : !hw.inout<i1>
        %26 = comb.concat %24, %22, %20, %18 : i1, i1, i1, i1
        %28 = sv.wire sym @test_when_lazy_array_slice.x name "x" : !hw.inout<i4>
        sv.assign %28, %26 : i4
        %27 = sv.read_inout %28 : !hw.inout<i4>
        %29 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %18, %29) : i1, i1, i1
        %30 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %20, %30) : i1, i1, i1
        %31 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %22, %31) : i1, i1, i1
        %32 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %24, %32) : i1, i1, i1
        %34 = hw.constant -1 : i1
        %33 = comb.xor %34, %S : i1
        %35 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%33, %18, %35) : i1, i1, i1
        %36 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%33, %20, %36) : i1, i1, i1
        %37 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%33, %22, %37) : i1, i1, i1
        %38 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%33, %24, %38) : i1, i1, i1
        hw.output %27 : i4
    }
}
