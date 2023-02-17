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
        hw.output %I_x, %I_y_0, %0 : i1, i1, i8
    }
}
