module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_array_assign(%I_x: i1, %I_y_0: i1, %I_y_1: i8, %S: i1) -> (O_x: i1, O_y_0: i1, O_y_1: i8) {
        %1 = sv.reg : !hw.inout<i8>
        %0 = sv.read_inout %1 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %S {
                %2 = comb.extract %I_y_1 from 0 : (i8) -> i1
                %3 = comb.extract %I_y_1 from 1 : (i8) -> i1
                %4 = comb.extract %I_y_1 from 2 : (i8) -> i1
                %5 = comb.extract %I_y_1 from 3 : (i8) -> i1
                %6 = comb.extract %I_y_1 from 4 : (i8) -> i1
                %7 = comb.extract %I_y_1 from 5 : (i8) -> i1
                %8 = comb.extract %I_y_1 from 6 : (i8) -> i1
                %9 = comb.extract %I_y_1 from 7 : (i8) -> i1
                %10 = comb.concat %9, %8, %7, %6, %5, %4, %3, %2 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %1, %10 : i8
            } else {
                %11 = comb.extract %I_y_1 from 7 : (i8) -> i1
                %12 = comb.extract %I_y_1 from 6 : (i8) -> i1
                %13 = comb.extract %I_y_1 from 5 : (i8) -> i1
                %14 = comb.extract %I_y_1 from 4 : (i8) -> i1
                %15 = comb.extract %I_y_1 from 3 : (i8) -> i1
                %16 = comb.extract %I_y_1 from 2 : (i8) -> i1
                %17 = comb.extract %I_y_1 from 1 : (i8) -> i1
                %18 = comb.extract %I_y_1 from 0 : (i8) -> i1
                %19 = comb.concat %18, %17, %16, %15, %14, %13, %12, %11 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %1, %19 : i8
            }
        }
        hw.output %I_x, %I_y_0, %0 : i1, i1, i8
    }
}
