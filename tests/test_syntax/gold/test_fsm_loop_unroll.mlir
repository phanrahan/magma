module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Foo(in %CLK: i1, out O: i2) {
        %1 = hw.struct_create (%0) : !hw.struct<tag: i2>
        %3 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<tag: i2>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : !hw.struct<tag: i2>
        }
        %5 = hw.constant 0 : i2
        %4 = hw.struct_create (%5) : !hw.struct<tag: i2>
        sv.initial {
            sv.bpassign %3, %4 : !hw.struct<tag: i2>
        }
        %2 = sv.read_inout %3 : !hw.inout<!hw.struct<tag: i2>>
        %6 = hw.struct_extract %2["tag"] : !hw.struct<tag: i2>
        %7 = hw.constant 0 : i2
        %8 = comb.icmp eq %6, %7 : i2
        %9 = hw.constant 0 : i2
        %10 = hw.constant 1 : i2
        %11 = hw.constant 1 : i2
        %12 = comb.icmp eq %6, %11 : i2
        %13 = hw.constant 1 : i2
        %14 = hw.constant 2 : i2
        %15 = hw.constant 2 : i2
        %16 = comb.icmp eq %6, %15 : i2
        %17 = hw.constant 2 : i2
        %18 = hw.constant 0 : i2
        %19 = hw.constant 3 : i2
        %21 = sv.reg : !hw.inout<i2>
        %20 = sv.read_inout %21 : !hw.inout<i2>
        %22 = sv.reg : !hw.inout<i2>
        %0 = sv.read_inout %22 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %8 {
                sv.bpassign %21, %9 : i2
                sv.bpassign %22, %10 : i2
            } else {
                sv.if %12 {
                    sv.bpassign %21, %13 : i2
                    sv.bpassign %22, %14 : i2
                } else {
                    sv.if %16 {
                        sv.bpassign %21, %17 : i2
                        sv.bpassign %22, %18 : i2
                    } else {
                        sv.bpassign %21, %19 : i2
                        sv.bpassign %22, %10 : i2
                    }
                }
            }
        }
        hw.output %20 : i2
    }
}
