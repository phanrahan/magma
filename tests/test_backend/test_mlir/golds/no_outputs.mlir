module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @no_outputs(%I: i1) -> () {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
    }
}
