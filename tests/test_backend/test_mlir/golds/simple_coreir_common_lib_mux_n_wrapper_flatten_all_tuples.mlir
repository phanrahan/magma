module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_coreir_common_lib_mux_n_wrapper(%I_data: !hw.array<8xi6>, %I_sel: i3) -> (O: i6) {
        %0 = hw.array_get %I_data[%I_sel] : !hw.array<8xi6>, i3
        hw.output %0 : i6
    }
}
