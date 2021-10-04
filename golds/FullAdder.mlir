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
