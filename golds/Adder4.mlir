hw.module @FullAdder(%a: i1, %b: i1, %cin: i1) -> (%sum_: i1, %cout: i1) {
    %0 = comb.xor %a, %b : i1
    %1 = comb.and %a, %b : i1
    %2 = comb.and %b, %cin : i1
    %3 = comb.and %a, %cin : i1
    %4 = comb.xor %0, %cin : i1
    %5 = comb.or %1, %2 : i1
    %6 = comb.or %5, %3 : i1
    hw.output %4, %6 : i1, i1
}
hw.module @Adder4(%A: i4, %B: i4, %CIN: i1) -> (%SUM: i4, %COUT: i1) {
    %0 = comb.extract %A from 0 : (i4) -> i1
    %1 = comb.extract %A from 1 : (i4) -> i1
    %2 = comb.extract %A from 2 : (i4) -> i1
    %3 = comb.extract %A from 3 : (i4) -> i1
    %4 = comb.extract %B from 0 : (i4) -> i1
    %5 = comb.extract %B from 1 : (i4) -> i1
    %6 = comb.extract %B from 2 : (i4) -> i1
    %7 = comb.extract %B from 3 : (i4) -> i1
    %8, %9 = hw.instance "FullAdder_inst0" @FullAdder(%0, %4, %CIN) : (i1, i1, i1) -> (i1, i1)
    %11, %10 = hw.instance "FullAdder_inst1" @FullAdder(%1, %5, %9) : (i1, i1, i1) -> (i1, i1)
    %13, %12 = hw.instance "FullAdder_inst2" @FullAdder(%2, %6, %10) : (i1, i1, i1) -> (i1, i1)
    %15, %14 = hw.instance "FullAdder_inst3" @FullAdder(%3, %7, %12) : (i1, i1, i1) -> (i1, i1)
    %16 = comb.concat %15, %13, %11, %8 : (i1, i1, i1, i1) -> i4
    hw.output %16, %14 : i4, i1
}
