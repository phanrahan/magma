hw.module @test_when_nested_Tuplex_Bits2_y_Bit(%I_0_x: i2, %I_0_y: i1, %I_1_x: i2, %I_1_y: i1, %S: i1) -> (O_x: i2, O_y: i1) {
    %0 = comb.extract %I_1_x from 0 : (i2) -> i1
    %1 = comb.extract %I_0_x from 0 : (i2) -> i1
    %2 = comb.extract %I_1_x from 1 : (i2) -> i1
    %3 = comb.extract %I_0_x from 1 : (i2) -> i1
    %7 = sv.reg : !hw.inout<i1>
    %4 = sv.read_inout %7 : !hw.inout<i1>
    %8 = sv.reg : !hw.inout<i1>
    %5 = sv.read_inout %8 : !hw.inout<i1>
    %9 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %9 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %7, %0 : i1
        sv.bpassign %8, %2 : i1
        sv.bpassign %9, %I_1_y : i1
        sv.if %S {
            sv.bpassign %7, %1 : i1
            sv.bpassign %8, %3 : i1
            sv.bpassign %9, %I_0_y : i1
        }
    }
    %10 = comb.concat %5, %4 : i1, i1
    hw.output %10, %6 : i2, i1
}
