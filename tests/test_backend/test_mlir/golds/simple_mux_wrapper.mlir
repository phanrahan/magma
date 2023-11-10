module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_mux_wrapper(in %a: i8, in %s: i1, out y: i8) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %a : i8
        %3 = hw.array_create %0, %a : i8
        %2 = hw.array_get %3[%s] : !hw.array<2xi8>, i1
        hw.output %2 : i8
    }
}
