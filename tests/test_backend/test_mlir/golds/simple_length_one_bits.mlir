hw.module @simple_length_one_bits(%I: i1) -> (O: i1) {
    %0 = comb.concat %I : i1
    %1 = hw.array_concat %0 : i1
    hw.output %1 : i1
}
