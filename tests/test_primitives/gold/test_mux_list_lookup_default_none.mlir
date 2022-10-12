hw.module @test_mux_list_lookup_default_none(%S: i2) -> (O: i5) {
    %0 = hw.constant 2 : i5
    %1 = hw.constant 1 : i5
    %2 = hw.constant 1 : i2
    %3 = comb.icmp eq %S, %2 : i2
    %5 = hw.array_create %1, %0 : i5
    %4 = hw.array_get %5[%3] : !hw.array<2xi5>
    %6 = hw.constant 0 : i5
    %7 = hw.constant 0 : i2
    %8 = comb.icmp eq %S, %7 : i2
    %10 = hw.array_create %6, %4 : i5
    %9 = hw.array_get %10[%8] : !hw.array<2xi5>
    hw.output %9 : i5
}
