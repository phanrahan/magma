module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_array_slice(in %a: !hw.array<12xi8>, out y: !hw.array<4xi8>) {
        %1 = hw.constant 0 : i4
        %0 = hw.array_slice %a[%1] : (!hw.array<12xi8>) -> !hw.array<4xi8>
        hw.output %0 : !hw.array<4xi8>
    }
}
