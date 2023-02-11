module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_partial_assign_order(%I: i2, %S: i2) -> (O0: i2, O1: i2, O2: i2) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = hw.constant -1 : i2
        %1 = comb.xor %2, %I : i2
        %3 = comb.extract %1 from 1 : (i2) -> i1
        %4 = comb.extract %1 from 0 : (i2) -> i1
        %5 = comb.extract %S from 1 : (i2) -> i1
        %6 = comb.xor %2, %I : i2
        %7 = comb.extract %6 from 0 : (i2) -> i1
        %8 = comb.extract %6 from 1 : (i2) -> i1
        %9 = comb.xor %2, %I : i2
        %10 = comb.extract %9 from 0 : (i2) -> i1
        %11 = comb.extract %9 from 1 : (i2) -> i1
        %17 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i2>
        %14 = sv.read_inout %19 : !hw.inout<i2>
        %20 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %21 : !hw.inout<i1>
        sv.alwayscomb {
            %22 = comb.extract %I from 0 : (i2) -> i1
            %23 = comb.extract %I from 1 : (i2) -> i1
            sv.bpassign %20, %22 : i1
            sv.bpassign %21, %23 : i1
            sv.if %0 {
                %24 = comb.extract %I from 0 : (i2) -> i1
                %25 = comb.extract %I from 1 : (i2) -> i1
                sv.bpassign %17, %3 : i1
                sv.bpassign %18, %4 : i1
                %26 = comb.concat %25, %24 : i1, i1
                sv.bpassign %19, %26 : i2
            } else {
                sv.if %5 {
                    %27 = comb.extract %I from 0 : (i2) -> i1
                    %28 = comb.extract %I from 1 : (i2) -> i1
                    %29 = comb.extract %I from 0 : (i2) -> i1
                    %30 = comb.extract %I from 1 : (i2) -> i1
                    sv.bpassign %17, %27 : i1
                    sv.bpassign %18, %28 : i1
                    %31 = comb.concat %30, %29 : i1, i1
                    sv.bpassign %19, %31 : i2
                } else {
                    %32 = comb.extract %I from 1 : (i2) -> i1
                    %33 = comb.extract %I from 0 : (i2) -> i1
                    sv.bpassign %17, %7 : i1
                    sv.bpassign %18, %8 : i1
                    sv.bpassign %20, %32 : i1
                    sv.bpassign %21, %33 : i1
                    %34 = comb.concat %11, %10 : i1, i1
                    sv.bpassign %19, %34 : i2
                }
            }
        }
        %35 = comb.concat %16, %15 : i1, i1
        %36 = comb.concat %13, %12 : i1, i1
        hw.output %35, %36, %14 : i2, i2, i2
    }
}
