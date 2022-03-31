hw.module @simple_array_of_bit(%I: i8) -> (O: i8) {
    %0 = comb.extract %I from 7 : (i8) -> i1
    %1 = comb.concat %0 : i1
    %2 = comb.extract %I from 6 : (i8) -> i1
    %3 = comb.concat %2 : i1
    %4 = comb.extract %I from 5 : (i8) -> i1
    %5 = comb.concat %4 : i1
    %6 = comb.extract %I from 4 : (i8) -> i1
    %7 = comb.concat %6 : i1
    %8 = comb.extract %I from 3 : (i8) -> i1
    %9 = comb.concat %8 : i1
    %10 = comb.extract %I from 2 : (i8) -> i1
    %11 = comb.concat %10 : i1
    %12 = comb.extract %I from 1 : (i8) -> i1
    %13 = comb.concat %12 : i1
    %14 = comb.extract %I from 0 : (i8) -> i1
    %15 = comb.concat %14 : i1
    %16 = hw.array_concat %15, %13, %11, %9, %7, %5, %3, %1 : i1, i1, i1, i1, i1, i1, i1, i1
    hw.output %16 : i8
}
