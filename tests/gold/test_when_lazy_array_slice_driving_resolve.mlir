module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
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
        %11 = sv.wire sym @test_when_lazy_array_slice_driving_resolve._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %11, %9 : i1
        %10 = sv.read_inout %11 : !hw.inout<i1>
        %12 = comb.extract %5 from 2 : (i4) -> i1
        %14 = sv.wire sym @test_when_lazy_array_slice_driving_resolve._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %14, %12 : i1
        %13 = sv.read_inout %14 : !hw.inout<i1>
        %15 = comb.extract %5 from 3 : (i4) -> i1
        %17 = sv.wire sym @test_when_lazy_array_slice_driving_resolve._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %17, %15 : i1
        %16 = sv.read_inout %17 : !hw.inout<i1>
        %18 = comb.concat %16, %13, %10, %0 : i1, i1, i1, i1
        %20 = sv.wire sym @test_when_lazy_array_slice_driving_resolve.x name "x" : !hw.inout<i4>
        sv.assign %20, %18 : i4
        %19 = sv.read_inout %20 : !hw.inout<i4>
        %21 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %21) : i1, i1, i1
        %22 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %13, %22) : i1, i1, i1
        %23 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %16, %23) : i1, i1, i1
        %25 = hw.constant -1 : i1
        %24 = comb.xor %25, %S : i1
        %26 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%24, %10, %26) : i1, i1, i1
        %27 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%24, %13, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%24, %16, %28) : i1, i1, i1
        hw.output %19 : i4
    }
}
