module attributes {circt.loweringOptions = "locationInfoStyle=wrapInAtSquareBracket"} {
    hw.module @simple_comb(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) {
        %1 = hw.constant -1 : i16
        loc("file.py":100:0)
        %0 = comb.xor %1, %a : i16
        loc("file.py":100:0)
        %2 = comb.or %a, %0 : i16
        loc("file.py":101:0)
        %3 = comb.or %2, %b : i16
        loc("file.py":102:0)
        hw.output %3, %3 : i16, i16
        loc(unknown)
    }
    loc("file.py":100:0)
}
loc(unknown)
