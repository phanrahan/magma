module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_overlap(%I: i4, %S: i1) -> (O: i4) {
        %1 = sv.reg : !hw.inout<i4>
        %0 = sv.read_inout %1 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %5 = comb.concat %4, %3, %2 : i1, i1, i2
                sv.bpassign %1, %5 : i4
            } else {
                %9 = comb.concat %8, %7, %6 : i1, i1, i2
                sv.bpassign %1, %9 : i4
            }
        }
        %2 = comb.extract %I from 0 : (i4) -> i2
        %3 = comb.extract %I from 2 : (i4) -> i1
        %4 = comb.extract %I from 3 : (i4) -> i1
        %6 = comb.extract %I from 2 : (i4) -> i2
        %7 = comb.extract %I from 0 : (i4) -> i1
        %8 = comb.extract %I from 1 : (i4) -> i1
        %10 = comb.extract %0 from 0 : (i4) -> i2
        %12 = sv.wire sym @test_when_lazy_array_slice_overlap._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i2>
        sv.assign %12, %10 : i2
        %11 = sv.read_inout %12 : !hw.inout<i2>
        %13 = comb.extract %11 from 0 : (i2) -> i1
        %14 = comb.extract %11 from 1 : (i2) -> i1
        %15 = comb.extract %0 from 2 : (i4) -> i1
        %17 = sv.wire sym @test_when_lazy_array_slice_overlap._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %17, %15 : i1
        %16 = sv.read_inout %17 : !hw.inout<i1>
        %18 = comb.extract %0 from 3 : (i4) -> i1
        %20 = sv.wire sym @test_when_lazy_array_slice_overlap._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %20, %18 : i1
        %19 = sv.read_inout %20 : !hw.inout<i1>
        %21 = comb.concat %19, %16, %14, %13 : i1, i1, i1, i1
        %22 = comb.extract %I from 0 : (i4) -> i1
        %23 = comb.extract %I from 1 : (i4) -> i1
        %24 = comb.concat %23, %22 : i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %11, %24) : i1, i2, i2
        %25 = comb.extract %I from 2 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %16, %25) : i1, i1, i1
        %26 = comb.extract %I from 3 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %19, %26) : i1, i1, i1
        %28 = hw.constant -1 : i1
        %27 = comb.xor %28, %S : i1
        %29 = comb.concat %26, %25 : i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %11, %29) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %16, %22) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %19, %23) : i1, i1, i1
        hw.output %21 : i4
    }
}
