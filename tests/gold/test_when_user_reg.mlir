module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Register(%I: i8, %CLK: i1) -> (O: i8)
    hw.module @test_when_user_reg(%I: i8, %x: i1, %CLK: i1) -> (O: i8) {
        %2 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %2 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i8
            sv.if %x {
                sv.bpassign %2, %I : i8
            }
        }
        %0 = hw.instance "x" @Register(I: %1: i8, CLK: %CLK: i1) -> (O: i8)
        hw.output %0 : i8
    }
}
