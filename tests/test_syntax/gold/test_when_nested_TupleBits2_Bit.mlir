hw.module @test_when_nested_TupleBits2_Bit(%I_0__0: i2, %I_0__1: i1, %I_1__0: i2, %I_1__1: i1, %S: i1) -> (O__0: i2, O__1: i1) {
    %2 = sv.reg : !hw.inout<i2>
    %0 = sv.read_inout %2 : !hw.inout<i2>
    %3 = sv.reg : !hw.inout<i1>
    %1 = sv.read_inout %3 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %2, %I_1__0 : i2
        sv.bpassign %3, %I_1__1 : i1
        sv.if %S {
            sv.bpassign %2, %I_0__0 : i2
            sv.bpassign %3, %I_0__1 : i1
        }
    }
    hw.output %0, %1 : i2, i1
}
