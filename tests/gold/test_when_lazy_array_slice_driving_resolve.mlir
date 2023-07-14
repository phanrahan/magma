module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_driving_resolve(%S: i1) -> (O: i4) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 2 : i4
        %2 = hw.constant 4 : i4
        %3 = hw.constant 0 : i1
        %4 = hw.constant 1 : i1
        %6 = sv.reg : !hw.inout<i4>
        %5 = sv.read_inout %6 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %7 = comb.concat %3, %3, %4, %3 : i1, i1, i1, i1
                sv.bpassign %6, %7 : i4
            } else {
                %8 = comb.concat %3, %4, %3, %3 : i1, i1, i1, i1
                sv.bpassign %6, %8 : i4
            }
        }
        %9 = comb.extract %5 from 1 : (i4) -> i1
        %10 = comb.extract %5 from 2 : (i4) -> i1
        %11 = comb.extract %5 from 3 : (i4) -> i1
        %12 = comb.concat %11, %10, %9, %0 : i1, i1, i1, i1
        %14 = sv.wire sym @test_when_lazy_array_slice_driving_resolve.x name "x" : !hw.inout<i4>
        sv.assign %14, %12 : i4
        %13 = sv.read_inout %14 : !hw.inout<i4>
        %16 = sv.wire sym @test_when_lazy_array_slice_driving_resolve._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %16, %9 : i1
        %15 = sv.read_inout %16 : !hw.inout<i1>
        %17 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %15, %17) : i1, i1, i1
        %19 = sv.wire sym @test_when_lazy_array_slice_driving_resolve._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %19, %10 : i1
        %18 = sv.read_inout %19 : !hw.inout<i1>
        %20 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %18, %20) : i1, i1, i1
        %22 = sv.wire sym @test_when_lazy_array_slice_driving_resolve._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %22, %11 : i1
        %21 = sv.read_inout %22 : !hw.inout<i1>
        %23 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %21, %23) : i1, i1, i1
        %25 = hw.constant -1 : i1
        %24 = comb.xor %25, %S : i1
        %26 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%24, %15, %26) : i1, i1, i1
        %27 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%24, %18, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%24, %21, %28) : i1, i1, i1
        hw.output %13 : i4
    }
}
