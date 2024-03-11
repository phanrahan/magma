module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_lazy_array_slice_overlap(in %I: i4, in %S: i1, out O: i4) {
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
        %13 = comb.extract %0 from 2 : (i4) -> i1
        %15 = sv.wire sym @test_when_lazy_array_slice_overlap._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %15, %13 : i1
        %14 = sv.read_inout %15 : !hw.inout<i1>
        %16 = comb.extract %0 from 3 : (i4) -> i1
        %18 = sv.wire sym @test_when_lazy_array_slice_overlap._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %18, %16 : i1
        %17 = sv.read_inout %18 : !hw.inout<i1>
        %19 = comb.concat %17, %14, %11 : i1, i1, i2
        %20 = comb.extract %I from 0 : (i4) -> i1
        %21 = comb.extract %I from 1 : (i4) -> i1
        %22 = comb.concat %21, %20 : i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %11, %22) : i1, i2, i2
        %23 = comb.extract %I from 2 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %14, %23) : i1, i1, i1
        %24 = comb.extract %I from 3 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %17, %24) : i1, i1, i1
        %26 = hw.constant -1 : i1
        %25 = comb.xor %26, %S : i1
        %27 = comb.concat %24, %23 : i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %11, %27) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %14, %20) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %17, %21) : i1, i1, i1
        hw.output %19 : i4
    }
}
