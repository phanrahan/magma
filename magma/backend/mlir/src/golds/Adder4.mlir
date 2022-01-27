hw.module @FullAdder(%a: i1, %b: i1, %cin: i1) -> (sum_: i1, cout: i1) {
    %0 = comb.xor %a, %b : i1
    %1 = comb.xor %0, %cin : i1
    %2 = comb.and %a, %b : i1
    %3 = comb.and %b, %cin : i1
    %4 = comb.or %2, %3 : i1
    %5 = comb.and %a, %cin : i1
    %6 = comb.or %4, %5 : i1
    hw.output %1, %6 : i1, i1
}
hw.module @Adder4(%A: i4, %B: i4, %CIN: i1) -> (SUM: i4, COUT: i1) {
    %0 = comb.extract %A from 0 : (i4) -> i1
    %1 = comb.extract %B from 0 : (i4) -> i1
    %2, %3 = hw.instance "FullAdder_inst0" @FullAdder(a: %0: i1, b: %1: i1, cin: %CIN: i1) -> (sum_: i1, cout: i1)
    %4 = comb.extract %A from 1 : (i4) -> i1
    %5 = comb.extract %B from 1 : (i4) -> i1
    %6, %7 = hw.instance "FullAdder_inst1" @FullAdder(a: %4: i1, b: %5: i1, cin: %3: i1) -> (sum_: i1, cout: i1)
    %8 = comb.extract %A from 2 : (i4) -> i1
    %9 = comb.extract %B from 2 : (i4) -> i1
    %10, %11 = hw.instance "FullAdder_inst2" @FullAdder(a: %8: i1, b: %9: i1, cin: %7: i1) -> (sum_: i1, cout: i1)
    %12 = comb.extract %A from 3 : (i4) -> i1
    %13 = comb.extract %B from 3 : (i4) -> i1
    %14, %15 = hw.instance "FullAdder_inst3" @FullAdder(a: %12: i1, b: %13: i1, cin: %11: i1) -> (sum_: i1, cout: i1)
    %16 = comb.concat %14, %10, %6, %2 : i1, i1, i1, i1
    hw.output %16, %15 : i4, i1
}
