module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Register(%I: i8, %CLK: i1) -> (O: i8) {
        %1 = sv.reg {name = "reg_P8_inst0"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i8
        }
        %2 = hw.constant 3 : i8
        sv.initial {
            sv.bpassign %1, %2 : i8
        }
        %0 = sv.read_inout %1 : !hw.inout<i8>
        hw.output %0 : i8
    }
    hw.module @simple_register_wrapper(%a: i8, %CLK: i1) -> (y: i8) {
        %0 = hw.instance "reg0" @Register(I: %a: i8, CLK: %CLK: i1) -> (O: i8)
        hw.output %0 : i8
    }
}
