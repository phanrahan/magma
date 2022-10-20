module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_multiple_whens(%I: i4, %S: i1) -> (O: i4) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %S : i1
        %2 = comb.extract %I from 0 : (i4) -> i1
        %3 = comb.extract %I from 1 : (i4) -> i1
        %4 = comb.extract %I from 2 : (i4) -> i1
        %5 = comb.extract %I from 3 : (i4) -> i1
        %11 = sv.reg : !hw.inout<i4>
        %6 = sv.read_inout %11 : !hw.inout<i4>
        %12 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %13 : !hw.inout<i1>
        %14 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %15 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %12, %2 : i1
                sv.bpassign %13, %3 : i1
                sv.bpassign %14, %4 : i1
                sv.bpassign %15, %5 : i1
            } else {
                sv.bpassign %12, %4 : i1
                sv.bpassign %13, %5 : i1
                sv.bpassign %14, %2 : i1
                sv.bpassign %15, %3 : i1
            }
        }
        %20 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg : !hw.inout<i1>
        %18 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %23 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %20, %7 : i1
            sv.bpassign %21, %8 : i1
            sv.bpassign %22, %9 : i1
            sv.bpassign %23, %10 : i1
            sv.if %0 {
                sv.bpassign %20, %2 : i1
                sv.bpassign %21, %3 : i1
                sv.bpassign %22, %4 : i1
                sv.bpassign %23, %5 : i1
            }
        }
        %24 = comb.concat %19, %18, %17, %16 : i1, i1, i1, i1
        hw.output %24 : i4
    }
}
