module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_array_assign(%I_x: i1, %I_y_0: i1, %I_y_1: i8, %S: i1) -> (O_x: i1, O_y_0: i1, O_y_1: i8) {
        %0 = comb.extract %I_y_1 from 0 : (i8) -> i1
        %1 = comb.extract %I_y_1 from 1 : (i8) -> i1
        %2 = comb.extract %I_y_1 from 2 : (i8) -> i1
        %3 = comb.extract %I_y_1 from 3 : (i8) -> i1
        %4 = comb.extract %I_y_1 from 4 : (i8) -> i1
        %5 = comb.extract %I_y_1 from 5 : (i8) -> i1
        %6 = comb.extract %I_y_1 from 6 : (i8) -> i1
        %7 = comb.extract %I_y_1 from 7 : (i8) -> i1
        %9 = sv.reg : !hw.inout<i8>
        %8 = sv.read_inout %9 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %S {
                %10 = comb.concat %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %9, %10 : i8
            } else {
                %11 = comb.concat %0, %1, %2, %3, %4, %5, %6, %7 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %9, %11 : i8
            }
        }
        hw.output %I_x, %I_y_0, %8 : i1, i1, i8
    }
}
