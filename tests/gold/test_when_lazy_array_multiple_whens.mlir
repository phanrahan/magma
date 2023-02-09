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
        %9 = sv.reg : !hw.inout<i4>
        %8 = sv.read_inout %9 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %10 = comb.concat %6, %5, %3, %2 : i1, i1, i1, i1
                sv.bpassign %9, %10 : i4
            } else {
                %11 = comb.concat %3, %2, %6, %5 : i1, i1, i1, i1
                sv.bpassign %9, %11 : i4
            }
        }
        %12 = comb.extract %8 from 0 : (i4) -> i1
        %13 = comb.extract %8 from 1 : (i4) -> i1
        %14 = comb.extract %8 from 2 : (i4) -> i1
        %15 = comb.extract %8 from 3 : (i4) -> i1
        %20 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg : !hw.inout<i1>
        %18 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %23 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %20, %12 : i1
            sv.bpassign %21, %13 : i1
            sv.bpassign %22, %14 : i1
            sv.bpassign %23, %15 : i1
            sv.if %0 {
                sv.bpassign %20, %2 : i1
                sv.bpassign %21, %3 : i1
                sv.bpassign %22, %5 : i1
                sv.bpassign %23, %6 : i1
            }
        }
        %24 = comb.concat %19, %18, %17, %16 : i1, i1, i1, i1
        hw.output %24 : i4
    }
}
