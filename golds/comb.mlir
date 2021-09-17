hw.module @comb(%y: i16, %z: i16) -> (%y: i16, %z: i16) {
    %0 = comb.not %a : i16
    %1 = comb.or %a, %0 : i16
    %2 = comb.or %1, %b : i16
    hw.output %2, %2 : i16, i16
}
