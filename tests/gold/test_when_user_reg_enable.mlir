module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Register(%I: i8, %CE: i1, %CLK: i1) -> (O: i8)
    hw.module @test_when_user_reg_enable(%I: i8, %x: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %x from 0 : (i2) -> i1
        %1 = hw.constant 1 : i1
        %2 = comb.extract %x from 1 : (i2) -> i1
        %4 = hw.constant -1 : i8
        %3 = comb.xor %4, %I : i8
        %5 = hw.constant 0 : i1
        %9 = sv.reg : !hw.inout<i8>
        %7 = sv.read_inout %9 : !hw.inout<i8>
        %10 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %10 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %6 : i8
            sv.bpassign %10, %5 : i1
            sv.if %0 {
                sv.bpassign %9, %I : i8
                sv.bpassign %10, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %9, %3 : i8
                    sv.bpassign %10, %1 : i1
                }
            }
        }
        %6 = hw.instance "Register_inst0" @Register(I: %7: i8, CE: %8: i1, CLK: %CLK: i1) -> (O: i8)
        hw.output %6 : i8
    }
}
