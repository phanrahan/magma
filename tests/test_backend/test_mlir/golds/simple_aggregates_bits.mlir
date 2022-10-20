module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_aggregates_bits(%a: i16) -> (y: i16, z: i8) {
        %0 = comb.extract %a from 8 : (i16) -> i1
        %1 = comb.extract %a from 9 : (i16) -> i1
        %2 = comb.extract %a from 10 : (i16) -> i1
        %3 = comb.extract %a from 11 : (i16) -> i1
        %4 = comb.extract %a from 12 : (i16) -> i1
        %5 = comb.extract %a from 13 : (i16) -> i1
        %6 = comb.extract %a from 14 : (i16) -> i1
        %7 = comb.extract %a from 15 : (i16) -> i1
        %8 = comb.extract %a from 0 : (i16) -> i1
        %9 = comb.extract %a from 1 : (i16) -> i1
        %10 = comb.extract %a from 2 : (i16) -> i1
        %11 = comb.extract %a from 3 : (i16) -> i1
        %12 = comb.extract %a from 4 : (i16) -> i1
        %13 = comb.extract %a from 5 : (i16) -> i1
        %14 = comb.extract %a from 6 : (i16) -> i1
        %15 = comb.extract %a from 7 : (i16) -> i1
        %16 = comb.concat %15, %14, %13, %12, %11, %10, %9, %8, %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %17 = comb.concat %15, %14, %13, %12, %11, %10, %9, %8 : i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %16, %17 : i16, i8
    }
}
