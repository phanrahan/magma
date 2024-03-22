module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Foo(in %CLK: i1, out O: i16) {
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
        %9 = hw.constant 65261 : i16
        %10 = hw.constant 2 : i2
        %11 = hw.constant 2 : i2
        %12 = comb.icmp eq %6, %11 : i2
        %13 = hw.constant 57005 : i16
        %14 = hw.constant 0 : i1
        %15 = hw.constant 1 : i1
        %18 = sv.reg name "Register_inst1" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %18, %16 : i1
        }
        %19 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %18, %19 : i1
        }
        %17 = sv.read_inout %18 : !hw.inout<i1>
        %20 = hw.constant 48879 : i16
        %21 = hw.constant 1 : i2
        %22 = hw.constant 1 : i2
        %23 = comb.icmp eq %6, %22 : i2
        %24 = hw.constant 48879 : i16
        %27 = sv.reg name "Register_inst2" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %27, %25 : i1
        }
        sv.initial {
            sv.bpassign %27, %19 : i1
        }
        %26 = sv.read_inout %27 : !hw.inout<i1>
        %28 = hw.constant 57005 : i16
        %29 = hw.constant 3 : i2
        %30 = hw.constant 57069 : i16
        %32 = sv.reg : !hw.inout<i16>
        %31 = sv.read_inout %32 : !hw.inout<i16>
        %33 = sv.reg : !hw.inout<i2>
        %0 = sv.read_inout %33 : !hw.inout<i2>
        %34 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %34 : !hw.inout<i1>
        %35 = sv.reg : !hw.inout<i1>
        %25 = sv.read_inout %35 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %34, %14 : i1
            sv.bpassign %35, %14 : i1
            sv.bpassign %33, %6 : i2
            sv.if %8 {
                sv.bpassign %32, %9 : i16
                sv.bpassign %33, %10 : i2
            } else {
                sv.if %12 {
                    sv.bpassign %32, %13 : i16
                    sv.bpassign %34, %15 : i1
                    sv.if %17 {
                        sv.bpassign %32, %20 : i16
                        sv.bpassign %33, %21 : i2
                    }
                } else {
                    sv.if %23 {
                        sv.bpassign %32, %24 : i16
                        sv.bpassign %35, %15 : i1
                        sv.if %26 {
                            sv.bpassign %32, %28 : i16
                            sv.bpassign %33, %29 : i2
                        }
                    } else {
                        sv.bpassign %32, %30 : i16
                        sv.bpassign %33, %29 : i2
                    }
                }
            }
        }
        hw.output %31 : i16
    }
}
