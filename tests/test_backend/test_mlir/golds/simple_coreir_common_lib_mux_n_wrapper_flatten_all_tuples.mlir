module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_coreir_common_lib_mux_n_wrapper(in %I_data: !hw.array<8xi6>, in %I_sel: i3, out O: i6) {
        %0 = hw.array_get %I_data[%I_sel] : !hw.array<8xi6>, i3
        hw.output %0 : i6
    }
}
