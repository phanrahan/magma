module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_structural(in %a: i16, in %b: i16, in %c: i16, in %CLK: i1, out y: i16, out z: i16) {
        %1 = sv.reg name "a_reg" : !hw.inout<i16>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %a : i16
        }
        %2 = hw.constant 0 : i16
        sv.initial {
            sv.bpassign %1, %2 : i16
        }
        %0 = sv.read_inout %1 : !hw.inout<i16>
        %3 = comb.and %0, %c : i16
        %4 = comb.or %0, %b : i16
        hw.output %3, %4 : i16, i16
    }
}
