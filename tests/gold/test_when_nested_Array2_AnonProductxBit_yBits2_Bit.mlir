module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit(%I_0_0_x: i1, %I_0_0_y: i2, %I_0_1_x: i1, %I_0_1_y: i2, %I_1_0_x: i1, %I_1_0_y: i2, %I_1_1_x: i1, %I_1_1_y: i2, %S: i1) -> (O_0_x: i1, O_0_y: i2, O_1_x: i1, O_1_y: i2) {
        %8 = sv.reg : !hw.inout<i1>
        %0 = sv.read_inout %8 : !hw.inout<i1>
        %9 = sv.reg : !hw.inout<i2>
        %1 = sv.read_inout %9 : !hw.inout<i2>
        %10 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %10 : !hw.inout<i1>
        %11 = sv.reg : !hw.inout<i2>
        %3 = sv.read_inout %11 : !hw.inout<i2>
        %12 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i2>
        %5 = sv.read_inout %13 : !hw.inout<i2>
        %14 = sv.reg : !hw.inout<i1>
        %6 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg : !hw.inout<i2>
        %7 = sv.read_inout %15 : !hw.inout<i2>
        sv.alwayscomb {
            sv.bpassign %12, %I_1_0_x : i1
            sv.bpassign %13, %I_1_0_y : i2
            sv.bpassign %14, %I_1_1_x : i1
            sv.bpassign %15, %I_1_1_y : i2
            sv.bpassign %12, %I_1_0_x : i1
            sv.bpassign %13, %I_1_0_y : i2
            sv.bpassign %14, %I_1_1_x : i1
            sv.bpassign %15, %I_1_1_y : i2
            sv.if %S {
                sv.bpassign %12, %I_0_0_x : i1
                sv.bpassign %13, %I_0_0_y : i2
                sv.bpassign %14, %I_0_1_x : i1
                sv.bpassign %15, %I_0_1_y : i2
            }
        }
        hw.output %4, %5, %6, %7 : i1, i2, i1, i2
    }
}
