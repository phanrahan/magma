hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit(%I_0_0_x: i1, %I_0_0_y: i2, %I_0_1_x: i1, %I_0_1_y: i2, %I_1_0_x: i1, %I_1_0_y: i2, %I_1_1_x: i1, %I_1_1_y: i2, %S: i1) -> (O_0_x: i1, O_0_y: i2, O_1_x: i1, O_1_y: i2) {
    %0 = comb.extract %I_1_0_y from 0 : (i2) -> i1
    %1 = comb.extract %I_0_0_y from 0 : (i2) -> i1
    %2 = comb.extract %I_1_0_y from 1 : (i2) -> i1
    %3 = comb.extract %I_0_0_y from 1 : (i2) -> i1
    %4 = comb.extract %I_1_1_y from 0 : (i2) -> i1
    %5 = comb.extract %I_0_1_y from 0 : (i2) -> i1
    %6 = comb.extract %I_1_1_y from 1 : (i2) -> i1
    %7 = comb.extract %I_0_1_y from 1 : (i2) -> i1
    %14 = sv.reg : !hw.inout<i1>
    %8 = sv.read_inout %14 : !hw.inout<i1>
    %15 = sv.reg : !hw.inout<i1>
    %9 = sv.read_inout %15 : !hw.inout<i1>
    %16 = sv.reg : !hw.inout<i1>
    %10 = sv.read_inout %16 : !hw.inout<i1>
    %17 = sv.reg : !hw.inout<i1>
    %11 = sv.read_inout %17 : !hw.inout<i1>
    %18 = sv.reg : !hw.inout<i1>
    %12 = sv.read_inout %18 : !hw.inout<i1>
    %19 = sv.reg : !hw.inout<i1>
    %13 = sv.read_inout %19 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %14, %I_1_0_x : i1
        sv.bpassign %15, %0 : i1
        sv.bpassign %16, %2 : i1
        sv.bpassign %17, %I_1_1_x : i1
        sv.bpassign %18, %4 : i1
        sv.bpassign %19, %6 : i1
        sv.if %S {
            sv.bpassign %14, %I_0_0_x : i1
            sv.bpassign %15, %1 : i1
            sv.bpassign %16, %3 : i1
            sv.bpassign %17, %I_0_1_x : i1
            sv.bpassign %18, %5 : i1
            sv.bpassign %19, %7 : i1
        }
    }
    %20 = comb.concat %10, %9 : i1, i1
    %21 = comb.concat %13, %12 : i1, i1
    hw.output %8, %20, %11, %21 : i1, i2, i1, i2
}
