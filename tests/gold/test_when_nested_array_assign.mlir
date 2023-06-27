module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_array_assign(%I_x: i1, %I_y_0: i1, %I_y_1: i8, %S: i1) -> (O_x: i1, O_y_0: i1, O_y_1: i8) {
        %1 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
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
        %13 = comb.extract %I_y_1 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %13) : i1, i1, i1
        %14 = comb.extract %0 from 1 : (i8) -> i1
        %15 = comb.extract %I_y_1 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %14, %15) : i1, i1, i1
        %16 = comb.extract %0 from 2 : (i8) -> i1
        %17 = comb.extract %I_y_1 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %16, %17) : i1, i1, i1
        %18 = comb.extract %0 from 3 : (i8) -> i1
        %19 = comb.extract %I_y_1 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %18, %19) : i1, i1, i1
        %20 = comb.extract %0 from 4 : (i8) -> i1
        %21 = comb.extract %I_y_1 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %20, %21) : i1, i1, i1
        %22 = comb.extract %0 from 5 : (i8) -> i1
        %23 = comb.extract %I_y_1 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %22, %23) : i1, i1, i1
        %24 = comb.extract %0 from 6 : (i8) -> i1
        %25 = comb.extract %I_y_1 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %24, %25) : i1, i1, i1
        %26 = comb.extract %0 from 7 : (i8) -> i1
        %27 = comb.extract %I_y_1 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %26, %27) : i1, i1, i1
        %29 = hw.constant -1 : i1
        %28 = comb.xor %29, %S : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %12, %27) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %14, %25) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %16, %23) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %18, %21) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %20, %19) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %22, %17) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %24, %15) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %26, %13) : i1, i1, i1
        hw.output %I_x, %I_y_0, %0 : i1, i1, i8
    }
}
