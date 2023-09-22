module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_lazy_array_slice_driving_resolve_2(%I: i4, %S: i1) -> (O: i4) {
        %0 = hw.constant 4 : i4
        %1 = hw.constant 0 : i1
        %2 = hw.constant 1 : i1
        %4 = sv.reg : !hw.inout<i4>
        %3 = sv.read_inout %4 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %9 = comb.concat %8, %7, %6, %5 : i1, i1, i1, i1
                sv.bpassign %4, %9 : i4
            } else {
                %10 = comb.concat %1, %2, %1, %1 : i1, i1, i1, i1
                sv.bpassign %4, %10 : i4
            }
        }
        %5 = comb.extract %I from 0 : (i4) -> i1
        %6 = comb.extract %I from 1 : (i4) -> i1
        %7 = comb.extract %I from 2 : (i4) -> i1
        %8 = comb.extract %I from 3 : (i4) -> i1
        %11 = comb.extract %3 from 0 : (i4) -> i1
        %13 = sv.wire sym @test_when_lazy_array_slice_driving_resolve_2._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %13, %11 : i1
        %12 = sv.read_inout %13 : !hw.inout<i1>
        %14 = comb.extract %3 from 1 : (i4) -> i1
        %16 = sv.wire sym @test_when_lazy_array_slice_driving_resolve_2._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %16, %14 : i1
        %15 = sv.read_inout %16 : !hw.inout<i1>
        %17 = comb.extract %3 from 2 : (i4) -> i1
        %19 = sv.wire sym @test_when_lazy_array_slice_driving_resolve_2._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %19, %17 : i1
        %18 = sv.read_inout %19 : !hw.inout<i1>
        %20 = comb.extract %I from 0 : (i4) -> i1
        %21 = comb.concat %20, %18, %15, %12 : i1, i1, i1, i1
        %23 = sv.wire sym @test_when_lazy_array_slice_driving_resolve_2.x name "x" : !hw.inout<i4>
        sv.assign %23, %21 : i4
        %22 = sv.read_inout %23 : !hw.inout<i4>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %20) : i1, i1, i1
        %24 = comb.extract %I from 1 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %15, %24) : i1, i1, i1
        %25 = comb.extract %I from 2 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %18, %25) : i1, i1, i1
        %27 = hw.constant -1 : i1
        %26 = comb.xor %27, %S : i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%26, %12, %28) : i1, i1, i1
        %29 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%26, %15, %29) : i1, i1, i1
        %30 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%26, %18, %30) : i1, i1, i1
        hw.output %22 : i4
    }
}
