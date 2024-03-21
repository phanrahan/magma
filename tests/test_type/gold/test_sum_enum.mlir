module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Foo(in %CLK: i1, out O: i16) {
        %2 = sv.reg name "Register_inst0" : !hw.inout<i2>
        sv.alwaysff(posedge %CLK) {
            sv.passign %2, %0 : i2
        }
        %3 = hw.constant 0 : i2
        sv.initial {
            sv.bpassign %2, %3 : i2
        }
        %1 = sv.read_inout %2 : !hw.inout<i2>
        %4 = hw.constant 0 : i2
        %5 = comb.icmp eq %1, %4 : i2
        %6 = hw.constant 65261 : i16
        %7 = hw.constant 1 : i2
        %8 = hw.constant 1 : i2
        %9 = comb.icmp eq %1, %8 : i2
        %10 = hw.constant 57005 : i16
        %11 = hw.constant 2 : i2
        %12 = hw.constant 48879 : i16
        %14 = sv.reg : !hw.inout<i16>
        %13 = sv.read_inout %14 : !hw.inout<i16>
        %15 = sv.reg : !hw.inout<i2>
        %0 = sv.read_inout %15 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %5 {
                sv.bpassign %14, %6 : i16
                sv.bpassign %15, %7 : i2
            } else {
                sv.if %9 {
                    sv.bpassign %14, %10 : i16
                    sv.bpassign %15, %11 : i2
                } else {
                    sv.bpassign %14, %12 : i16
                    sv.bpassign %15, %11 : i2
                }
            }
        }
        hw.output %13 : i16
    }
}
