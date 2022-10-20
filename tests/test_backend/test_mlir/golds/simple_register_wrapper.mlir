module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_register_wrapper(%a: i8, %CLK: i1) -> (y: i8) {
        %1 = sv.reg {name = "reg0"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %a : i8
        }
        %2 = hw.constant 3 : i8
        sv.initial {
            sv.bpassign %1, %2 : i8
        }
        %0 = sv.read_inout %1 : !hw.inout<i8>
        hw.output %0 : i8
    }
}
