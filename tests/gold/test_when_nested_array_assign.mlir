module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_array_assign(%I_x: i1, %I_y_0: i1, %I_y_1: i8, %S: i1) -> (O_x: i1, O_y_0: i1, O_y_1: i8) {
        %1 = sv.reg : !hw.inout<i8>
        %0 = sv.read_inout %1 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %S {
                %10 = comb.concat %9, %8, %7, %6, %5, %4, %3, %2 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %1, %10 : i8
            } else {
                %11 = comb.concat %2, %3, %4, %5, %6, %7, %8, %9 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %1, %11 : i8
            }
        }
        %2 = comb.extract %I_y_1 from 0 : (i8) -> i1
        %3 = comb.extract %I_y_1 from 1 : (i8) -> i1
        %4 = comb.extract %I_y_1 from 2 : (i8) -> i1
        %5 = comb.extract %I_y_1 from 3 : (i8) -> i1
        %6 = comb.extract %I_y_1 from 4 : (i8) -> i1
        %7 = comb.extract %I_y_1 from 5 : (i8) -> i1
        %8 = comb.extract %I_y_1 from 6 : (i8) -> i1
        %9 = comb.extract %I_y_1 from 7 : (i8) -> i1
        %12 = comb.extract %0 from 0 : (i8) -> i1
        %14 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %14, %12 : i1
        %13 = sv.read_inout %14 : !hw.inout<i1>
        %15 = comb.extract %0 from 1 : (i8) -> i1
        %17 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %17, %15 : i1
        %16 = sv.read_inout %17 : !hw.inout<i1>
        %18 = comb.extract %0 from 2 : (i8) -> i1
        %20 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %20, %18 : i1
        %19 = sv.read_inout %20 : !hw.inout<i1>
        %21 = comb.extract %0 from 3 : (i8) -> i1
        %23 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %23, %21 : i1
        %22 = sv.read_inout %23 : !hw.inout<i1>
        %24 = comb.extract %0 from 4 : (i8) -> i1
        %26 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %26, %24 : i1
        %25 = sv.read_inout %26 : !hw.inout<i1>
        %27 = comb.extract %0 from 5 : (i8) -> i1
        %29 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %29, %27 : i1
        %28 = sv.read_inout %29 : !hw.inout<i1>
        %30 = comb.extract %0 from 6 : (i8) -> i1
        %32 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %32, %30 : i1
        %31 = sv.read_inout %32 : !hw.inout<i1>
        %33 = comb.extract %0 from 7 : (i8) -> i1
        %35 = sv.wire sym @test_when_nested_array_assign._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i1>
        sv.assign %35, %33 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %36 = comb.concat %34, %31, %28, %25, %22, %19, %16, %13 : i1, i1, i1, i1, i1, i1, i1, i1
        %37 = comb.extract %I_y_1 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %13, %37) : i1, i1, i1
        %38 = comb.extract %I_y_1 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %16, %38) : i1, i1, i1
        %39 = comb.extract %I_y_1 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %19, %39) : i1, i1, i1
        %40 = comb.extract %I_y_1 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %22, %40) : i1, i1, i1
        %41 = comb.extract %I_y_1 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %25, %41) : i1, i1, i1
        %42 = comb.extract %I_y_1 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %28, %42) : i1, i1, i1
        %43 = comb.extract %I_y_1 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %31, %43) : i1, i1, i1
        %44 = comb.extract %I_y_1 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %34, %44) : i1, i1, i1
        %46 = hw.constant -1 : i1
        %45 = comb.xor %46, %S : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %13, %44) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %16, %43) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %19, %42) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %22, %41) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %25, %40) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %28, %39) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %31, %38) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %34, %37) : i1, i1, i1
        hw.output %I_x, %I_y_0, %36 : i1, i1, i8
    }
}
