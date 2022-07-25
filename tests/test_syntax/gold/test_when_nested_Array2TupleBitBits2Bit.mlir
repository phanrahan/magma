hw.module @test_when_nested_Array2TupleBitBits2Bit(%I_0_0__0: i1, %I_0_0__1: i2, %I_0_1__0: i1, %I_0_1__1: i2, %I_1_0__0: i1, %I_1_0__1: i2, %I_1_1__0: i1, %I_1_1__1: i2, %S: i1) -> (O_0__0: i1, O_0__1: i2, O_1__0: i1, O_1__1: i2) {
    %4 = sv.reg {name = "O_0_reg"} : !hw.inout<i1>
    %5 = sv.reg {name = "O_1_reg"} : !hw.inout<i2>
    %6 = sv.reg {name = "O_2_reg"} : !hw.inout<i1>
    %7 = sv.reg {name = "O_3_reg"} : !hw.inout<i2>
    sv.alwayscomb {
        sv.bpassign %4, %I_1_0__0 : i1
        sv.bpassign %5, %I_1_0__1 : i2
        sv.bpassign %6, %I_1_1__0 : i1
        sv.bpassign %7, %I_1_1__1 : i2
        sv.if %S {
            sv.bpassign %4, %I_0_0__0 : i1
            sv.bpassign %5, %I_0_0__1 : i2
            sv.bpassign %6, %I_0_1__0 : i1
            sv.bpassign %7, %I_0_1__1 : i2
        }
    }
    %0 = sv.read_inout %4 : !hw.inout<i1>
    %1 = sv.read_inout %5 : !hw.inout<i2>
    %2 = sv.read_inout %6 : !hw.inout<i1>
    %3 = sv.read_inout %7 : !hw.inout<i2>
    hw.output %0, %1, %2, %3 : i1, i2, i1, i2
}
