hw.module @TestSliceInt(%I: i10) -> (O: i6) {
    %0 = comb.extract %I from 2 : (i10) -> i1
    %1 = comb.extract %I from 3 : (i10) -> i1
    %2 = comb.extract %I from 4 : (i10) -> i1
    %3 = comb.extract %I from 5 : (i10) -> i1
    %4 = comb.extract %I from 6 : (i10) -> i1
    %5 = comb.extract %I from 7 : (i10) -> i1
    %6 = comb.concat %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1
    hw.output %6 : i6
}
