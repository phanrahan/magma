module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_partial_assign_order(in %I: i2, in %S: i2, out O0: i2, out O1: i2, out O2: i2) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = hw.constant -1 : i2
        %1 = comb.xor %2, %I : i2
        %3 = comb.extract %1 from 1 : (i2) -> i1
        %4 = comb.extract %1 from 0 : (i2) -> i1
        %5 = comb.extract %S from 1 : (i2) -> i1
        %6 = comb.xor %2, %I : i2
        %7 = comb.extract %6 from 0 : (i2) -> i1
        %8 = comb.extract %6 from 1 : (i2) -> i1
        %9 = comb.xor %2, %I : i2
        %10 = comb.extract %9 from 0 : (i2) -> i1
        %11 = comb.extract %9 from 1 : (i2) -> i1
        %17 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i2>
        %14 = sv.read_inout %19 : !hw.inout<i2>
        %20 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %21 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %20, %22 : i1
            sv.bpassign %21, %23 : i1
            sv.if %0 {
                sv.bpassign %17, %3 : i1
                sv.bpassign %18, %4 : i1
                %24 = comb.concat %23, %22 : i1, i1
                sv.bpassign %19, %24 : i2
            } else {
                sv.if %5 {
                    sv.bpassign %17, %22 : i1
                    sv.bpassign %18, %23 : i1
                    %25 = comb.concat %23, %22 : i1, i1
                    sv.bpassign %19, %25 : i2
                } else {
                    sv.bpassign %17, %7 : i1
                    sv.bpassign %18, %8 : i1
                    sv.bpassign %20, %23 : i1
                    sv.bpassign %21, %22 : i1
                    %26 = comb.concat %11, %10 : i1, i1
                    sv.bpassign %19, %26 : i2
                }
            }
        }
        %22 = comb.extract %I from 0 : (i2) -> i1
        %23 = comb.extract %I from 1 : (i2) -> i1
        %28 = sv.wire sym @test_when_partial_assign_order._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %28, %15 : i1
        %27 = sv.read_inout %28 : !hw.inout<i1>
        %30 = sv.wire sym @test_when_partial_assign_order._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %30, %16 : i1
        %29 = sv.read_inout %30 : !hw.inout<i1>
        %31 = comb.concat %29, %27 : i1, i1
        %33 = sv.wire sym @test_when_partial_assign_order._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %33, %12 : i1
        %32 = sv.read_inout %33 : !hw.inout<i1>
        %35 = sv.wire sym @test_when_partial_assign_order._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %35, %13 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %36 = comb.concat %34, %32 : i1, i1
        %37 = comb.extract %14 from 0 : (i2) -> i1
        %39 = sv.wire sym @test_when_partial_assign_order._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %39, %37 : i1
        %38 = sv.read_inout %39 : !hw.inout<i1>
        %40 = comb.extract %14 from 1 : (i2) -> i1
        %42 = sv.wire sym @test_when_partial_assign_order._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %42, %40 : i1
        %41 = sv.read_inout %42 : !hw.inout<i1>
        %43 = comb.concat %41, %38 : i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %32, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %34, %4) : i1, i1, i1
        %44 = comb.extract %I from 0 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %38, %44) : i1, i1, i1
        %45 = comb.extract %I from 1 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %41, %45) : i1, i1, i1
        %47 = hw.constant -1 : i1
        %46 = comb.xor %47, %0 : i1
        %48 = comb.and %46, %5 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%48, %32, %44) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%48, %34, %45) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%48, %38, %44) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%48, %41, %45) : i1, i1, i1
        %49 = comb.xor %47, %5 : i1
        %50 = comb.and %46, %49 : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %32, %7) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %34, %8) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %27, %45) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %29, %44) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %38, %10) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %41, %11) : i1, i1, i1
        %51 = comb.xor %47, %50 : i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %27, %44) : i1, i1, i1
        %52 = comb.xor %47, %50 : i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%52, %29, %45) : i1, i1, i1
        hw.output %31, %36, %43 : i2, i2, i2
    }
}
