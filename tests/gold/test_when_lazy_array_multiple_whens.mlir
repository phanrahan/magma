module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_multiple_whens(%I: i4, %S: i1) -> (O: i4) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %S : i1
        %3 = sv.reg : !hw.inout<i4>
        %2 = sv.read_inout %3 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %4 = comb.extract %I from 2 : (i4) -> i1
                %5 = comb.extract %I from 3 : (i4) -> i1
                %6 = comb.extract %I from 0 : (i4) -> i1
                %7 = comb.extract %I from 1 : (i4) -> i1
                %8 = comb.concat %5, %4, %7, %6 : i1, i1, i1, i1
                sv.bpassign %3, %8 : i4
            } else {
                %9 = comb.extract %I from 0 : (i4) -> i1
                %10 = comb.extract %I from 1 : (i4) -> i1
                %11 = comb.extract %I from 2 : (i4) -> i1
                %12 = comb.extract %I from 3 : (i4) -> i1
                %13 = comb.concat %10, %9, %12, %11 : i1, i1, i1, i1
                sv.bpassign %3, %13 : i4
            }
        }
        %14 = comb.extract %2 from 0 : (i4) -> i1
        %15 = comb.extract %I from 0 : (i4) -> i1
        %16 = comb.extract %2 from 1 : (i4) -> i1
        %17 = comb.extract %I from 1 : (i4) -> i1
        %18 = comb.extract %2 from 2 : (i4) -> i1
        %19 = comb.extract %I from 2 : (i4) -> i1
        %20 = comb.extract %2 from 3 : (i4) -> i1
        %21 = comb.extract %I from 3 : (i4) -> i1
        %26 = sv.reg : !hw.inout<i1>
        %22 = sv.read_inout %26 : !hw.inout<i1>
        %27 = sv.reg : !hw.inout<i1>
        %23 = sv.read_inout %27 : !hw.inout<i1>
        %28 = sv.reg : !hw.inout<i1>
        %24 = sv.read_inout %28 : !hw.inout<i1>
        %29 = sv.reg : !hw.inout<i1>
        %25 = sv.read_inout %29 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %26, %14 : i1
            sv.bpassign %27, %16 : i1
            sv.bpassign %28, %18 : i1
            sv.bpassign %29, %20 : i1
            sv.if %0 {
                sv.bpassign %26, %15 : i1
                sv.bpassign %27, %17 : i1
                sv.bpassign %28, %19 : i1
                sv.bpassign %29, %21 : i1
            }
        }
        %30 = comb.concat %25, %24, %23, %22 : i1, i1, i1, i1
        hw.output %30 : i4
    }
}
