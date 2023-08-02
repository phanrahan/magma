module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_multiple_whens(%I: i4, %S: i1) -> (O: i4) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %S : i1
        %3 = sv.reg : !hw.inout<i4>
        %2 = sv.read_inout %3 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %8 = comb.concat %5, %4, %7, %6 : i1, i1, i1, i1
                sv.bpassign %3, %8 : i4
            } else {
                %9 = comb.concat %7, %6, %5, %4 : i1, i1, i1, i1
                sv.bpassign %3, %9 : i4
            }
        }
        %4 = comb.extract %I from 2 : (i4) -> i1
        %5 = comb.extract %I from 3 : (i4) -> i1
        %6 = comb.extract %I from 0 : (i4) -> i1
        %7 = comb.extract %I from 1 : (i4) -> i1
        %10 = comb.extract %2 from 0 : (i4) -> i1
        %12 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %12, %10 : i1
        %11 = sv.read_inout %12 : !hw.inout<i1>
        %13 = comb.extract %I from 0 : (i4) -> i1
        %14 = comb.extract %2 from 1 : (i4) -> i1
        %16 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %16, %14 : i1
        %15 = sv.read_inout %16 : !hw.inout<i1>
        %17 = comb.extract %I from 1 : (i4) -> i1
        %18 = comb.extract %2 from 2 : (i4) -> i1
        %20 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %20, %18 : i1
        %19 = sv.read_inout %20 : !hw.inout<i1>
        %21 = comb.extract %I from 2 : (i4) -> i1
        %22 = comb.extract %2 from 3 : (i4) -> i1
        %24 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %24, %22 : i1
        %23 = sv.read_inout %24 : !hw.inout<i1>
        %25 = comb.extract %I from 3 : (i4) -> i1
        %30 = sv.reg : !hw.inout<i1>
        %26 = sv.read_inout %30 : !hw.inout<i1>
        %31 = sv.reg : !hw.inout<i1>
        %27 = sv.read_inout %31 : !hw.inout<i1>
        %32 = sv.reg : !hw.inout<i1>
        %28 = sv.read_inout %32 : !hw.inout<i1>
        %33 = sv.reg : !hw.inout<i1>
        %29 = sv.read_inout %33 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %30, %11 : i1
            sv.bpassign %31, %15 : i1
            sv.bpassign %32, %19 : i1
            sv.bpassign %33, %23 : i1
            sv.if %0 {
                sv.bpassign %30, %13 : i1
                sv.bpassign %31, %17 : i1
                sv.bpassign %32, %21 : i1
                sv.bpassign %33, %25 : i1
            }
        }
        %35 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %35, %26 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %37 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %37, %27 : i1
        %36 = sv.read_inout %37 : !hw.inout<i1>
        %39 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %39, %28 : i1
        %38 = sv.read_inout %39 : !hw.inout<i1>
        %41 = sv.wire sym @test_when_lazy_array_multiple_whens._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %41, %29 : i1
        %40 = sv.read_inout %41 : !hw.inout<i1>
        %42 = comb.concat %40, %38, %36, %34 : i1, i1, i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %19, %21) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %23, %25) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %11, %13) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %15, %17) : i1, i1, i1
        %43 = comb.xor %1, %S : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%43, %19, %13) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%43, %23, %17) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%43, %11, %21) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%43, %15, %25) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %34, %13) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %36, %17) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %38, %21) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %40, %25) : i1, i1, i1
        %44 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %34, %10) : i1, i1, i1
        %45 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %36, %14) : i1, i1, i1
        %46 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%46, %38, %18) : i1, i1, i1
        %47 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %40, %22) : i1, i1, i1
        hw.output %42 : i4
    }
}
