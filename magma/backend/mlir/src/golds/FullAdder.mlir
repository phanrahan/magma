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
