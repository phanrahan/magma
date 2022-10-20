module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_length_one_array(%I: !hw.array<1xi8>) -> (O: i8) {
        %2 = hw.constant 0 : i8
        %1 = hw.array_create %2 : i8
        %3 = hw.array_concat %1, %I : !hw.array<1xi8>, !hw.array<1xi8>
        %4 = hw.constant 0 : i1
        %0 = hw.array_get %3[%4] : !hw.array<2xi8>, i1
        hw.output %0 : i8
    }
}
