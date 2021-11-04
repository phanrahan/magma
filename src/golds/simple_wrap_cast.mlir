hw.module @simple_wrap_cast(%I: i1) -> (%O: i1) {
    %0 = comb.merge %I : i1
    hw.output %0 : i1
}
