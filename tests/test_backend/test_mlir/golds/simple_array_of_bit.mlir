module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_array_of_bit(%I: i8) -> (O: i8) {
        %0 = comb.extract %I from 7 : (i8) -> i1
        %1 = comb.extract %I from 6 : (i8) -> i1
        %2 = comb.extract %I from 5 : (i8) -> i1
        %3 = comb.extract %I from 4 : (i8) -> i1
        %4 = comb.extract %I from 3 : (i8) -> i1
        %5 = comb.extract %I from 2 : (i8) -> i1
        %6 = comb.extract %I from 1 : (i8) -> i1
        %7 = comb.extract %I from 0 : (i8) -> i1
        %8 = comb.concat %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %8 : i8
    }
}
