module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_spurious_assign(%x: i8, %y: i1, %z: i2, %CLK: i1) -> (O_x: i8, O_y_x: i8, O_y_y: i1) {
        %0 = comb.extract %z from 0 : (i2) -> i1
        %1 = comb.extract %z from 1 : (i2) -> i1
        %2 = hw.constant 1 : i1
        %3 = hw.constant 1 : i8
        %5 = hw.constant -1 : i8
        %4 = comb.xor %5, %x : i8
        %8 = sv.reg : !hw.inout<i8>
        %6 = sv.read_inout %8 : !hw.inout<i8>
        %9 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %8, %x : i8
                } else {
                    sv.bpassign %8, %3 : i8
                }
            } else {
                sv.bpassign %8, %4 : i8
            }
        }
        %10 = hw.constant 1 : i1
        %12 = hw.constant -1 : i1
        %11 = comb.xor %12, %y : i1
        %15 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %16 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %1 {
                sv.bpassign %15, %y : i1
            } else {
                sv.bpassign %15, %11 : i1
            }
        }
        %20 = sv.reg {name = "reg"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %20, %x : i8
            }
        }
        %21 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %20, %21 : i8
        }
        %17 = sv.read_inout %20 : !hw.inout<i8>
        %22 = sv.reg {name = "reg"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %22, %6 : i8
            }
        }
        %23 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %22, %23 : i8
        }
        %18 = sv.read_inout %22 : !hw.inout<i8>
        %24 = sv.reg {name = "reg"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %24, %13 : i1
            }
        }
        %25 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %24, %25 : i1
        }
        %19 = sv.read_inout %24 : !hw.inout<i1>
        hw.output %17, %18, %19 : i8, i8, i1
    }
}
