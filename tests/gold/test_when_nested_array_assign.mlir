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
        %12 = comb.extract %I_y_1 from 0 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_260: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %13, %12) : i1, i1, i1
        %14 = comb.extract %I_y_1 from 1 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_261: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %15, %14) : i1, i1, i1
        %16 = comb.extract %I_y_1 from 2 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_262: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %17, %16) : i1, i1, i1
        %18 = comb.extract %I_y_1 from 3 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_263: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %19, %18) : i1, i1, i1
        %20 = comb.extract %I_y_1 from 4 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_264: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %21, %20) : i1, i1, i1
        %22 = comb.extract %I_y_1 from 5 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_265: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %23, %22) : i1, i1, i1
        %24 = comb.extract %I_y_1 from 6 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_266: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %25, %24) : i1, i1, i1
        %26 = comb.extract %I_y_1 from 7 : (i8) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_267: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %27, %26) : i1, i1, i1
        %29 = hw.constant -1 : i1
        %28 = comb.xor %29, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_268: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %13, %26) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_269: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %15, %24) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_270: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %17, %22) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_271: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %19, %20) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_272: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %21, %18) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_273: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %23, %16) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_274: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %25, %14) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_275: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %27, %12) : i1, i1, i1
        hw.output %I_x, %I_y_0, %0 : i1, i1, i8
    }
}
