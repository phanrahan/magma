module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_partial_assign_order(%I: i2, %S: i2) -> (O0: i2, O1: i2, O2: i2) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = hw.constant -1 : i2
        %1 = comb.xor %2, %I : i2
        %3 = comb.extract %1 from 1 : (i2) -> i1
        %4 = comb.extract %1 from 0 : (i2) -> i1
        %5 = comb.extract %S from 1 : (i2) -> i1
        %6 = comb.extract %I from 0 : (i2) -> i1
        %7 = comb.extract %I from 1 : (i2) -> i1
        %8 = comb.xor %2, %I : i2
        %9 = comb.extract %8 from 0 : (i2) -> i1
        %10 = comb.extract %8 from 1 : (i2) -> i1
        %11 = comb.xor %2, %I : i2
        %12 = comb.extract %11 from 0 : (i2) -> i1
        %13 = comb.extract %11 from 1 : (i2) -> i1
        %19 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i2>
        %16 = sv.read_inout %21 : !hw.inout<i2>
        %22 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i1>
        %18 = sv.read_inout %23 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %22, %6 : i1
            sv.bpassign %23, %7 : i1
            sv.if %0 {
                sv.bpassign %19, %3 : i1
                sv.bpassign %20, %4 : i1
                %24 = comb.concat %7, %6 : i1, i1
                sv.bpassign %21, %24 : i2
            } else {
                sv.if %5 {
                    sv.bpassign %19, %6 : i1
                    sv.bpassign %20, %7 : i1
                    %25 = comb.concat %7, %6 : i1, i1
                    sv.bpassign %21, %25 : i2
                } else {
                    sv.bpassign %19, %9 : i1
                    sv.bpassign %20, %10 : i1
                    sv.bpassign %22, %7 : i1
                    sv.bpassign %23, %6 : i1
                    %26 = comb.concat %13, %12 : i1, i1
                    sv.bpassign %21, %26 : i2
                }
            }
        }
        %27 = comb.concat %18, %17 : i1, i1
        %28 = comb.concat %15, %14 : i1, i1
        hw.output %27, %28, %16 : i2, i2, i2
    }
}
