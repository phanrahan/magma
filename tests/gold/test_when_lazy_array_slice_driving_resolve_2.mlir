module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_driving_resolve_2(%I: i4, %S: i1) -> (O: i4) {
        %0 = hw.constant 4 : i4
        %1 = comb.extract %I from 0 : (i4) -> i1
        %2 = hw.constant 0 : i1
        %3 = comb.extract %I from 1 : (i4) -> i1
        %4 = comb.extract %I from 2 : (i4) -> i1
        %5 = hw.constant 1 : i1
        %6 = comb.extract %I from 3 : (i4) -> i1
        %12 = sv.reg : !hw.inout<i4>
        %7 = sv.read_inout %12 : !hw.inout<i4>
        %13 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %13 : !hw.inout<i1>
        %14 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg : !hw.inout<i1>
        %11 = sv.read_inout %16 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %13, %1 : i1
                sv.bpassign %14, %3 : i1
                sv.bpassign %15, %4 : i1
                sv.bpassign %16, %6 : i1
            } else {
                sv.bpassign %13, %2 : i1
                sv.bpassign %14, %2 : i1
                sv.bpassign %15, %5 : i1
                sv.bpassign %16, %2 : i1
            }
        }
        %17 = comb.concat %1, %10, %9, %8 : i1, i1, i1, i1
        %19 = sv.wire sym @test_when_lazy_array_slice_driving_resolve_2.x {name="x"} : !hw.inout<i4>
        sv.assign %19, %17 : i4
        %18 = sv.read_inout %19 : !hw.inout<i4>
        hw.output %18 : i4
    }
}
