module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_multiple_whens(%I: i4, %S: i1) -> (O: i4) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %S : i1
        %2 = comb.extract %I from 0 : (i4) -> i1
        %3 = comb.extract %I from 1 : (i4) -> i1
        %4 = comb.concat %3, %2 : i1, i1
        %5 = comb.extract %I from 2 : (i4) -> i1
        %6 = comb.extract %I from 3 : (i4) -> i1
        %7 = comb.concat %6, %5 : i1, i1
        %14 = sv.reg : !hw.inout<i4>
        %8 = sv.read_inout %14 : !hw.inout<i4>
        %15 = sv.reg : !hw.inout<i2>
        %9 = sv.read_inout %15 : !hw.inout<i2>
        %16 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i1>
        %11 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %19 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %16, %5 : i1
                sv.bpassign %17, %6 : i1
                sv.bpassign %18, %2 : i1
                sv.bpassign %19, %3 : i1
            } else {
                sv.bpassign %16, %2 : i1
                sv.bpassign %17, %3 : i1
                sv.bpassign %18, %5 : i1
                sv.bpassign %19, %6 : i1
            }
        }
        %24 = sv.reg : !hw.inout<i1>
        %20 = sv.read_inout %24 : !hw.inout<i1>
        %25 = sv.reg : !hw.inout<i1>
        %21 = sv.read_inout %25 : !hw.inout<i1>
        %26 = sv.reg : !hw.inout<i1>
        %22 = sv.read_inout %26 : !hw.inout<i1>
        %27 = sv.reg : !hw.inout<i1>
        %23 = sv.read_inout %27 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %24, %12 : i1
            sv.bpassign %25, %13 : i1
            sv.bpassign %26, %10 : i1
            sv.bpassign %27, %11 : i1
            sv.if %0 {
                sv.bpassign %24, %2 : i1
                sv.bpassign %25, %3 : i1
                sv.bpassign %26, %5 : i1
                sv.bpassign %27, %6 : i1
            }
        }
        %28 = comb.concat %23, %22, %21, %20 : i1, i1, i1, i1
        hw.output %28 : i4
    }
}
