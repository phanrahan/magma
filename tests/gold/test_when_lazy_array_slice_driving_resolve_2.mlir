module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_driving_resolve_2(%I: i4, %S: i1) -> (O: i4) {
        %0 = hw.constant 4 : i4
        %1 = hw.constant 0 : i1
        %2 = hw.constant 1 : i1
        %4 = sv.reg : !hw.inout<i4>
        %3 = sv.read_inout %4 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %5 = comb.extract %I from 0 : (i4) -> i1
                %6 = comb.extract %I from 1 : (i4) -> i1
                %7 = comb.extract %I from 2 : (i4) -> i1
                %8 = comb.extract %I from 3 : (i4) -> i1
                %9 = comb.concat %8, %7, %6, %5 : i1, i1, i1, i1
                sv.bpassign %4, %9 : i4
            } else {
                %10 = comb.concat %1, %2, %1, %1 : i1, i1, i1, i1
                sv.bpassign %4, %10 : i4
            }
        }
        %11 = comb.extract %3 from 0 : (i4) -> i1
        %12 = comb.extract %3 from 1 : (i4) -> i1
        %13 = comb.extract %3 from 2 : (i4) -> i1
        %14 = comb.extract %I from 0 : (i4) -> i1
        %15 = comb.concat %14, %13, %12, %11 : i1, i1, i1, i1
        %17 = sv.wire sym @test_when_lazy_array_slice_driving_resolve_2.x {name="x"} : !hw.inout<i4>
        sv.assign %17, %15 : i4
        %16 = sv.read_inout %17 : !hw.inout<i4>
        hw.output %16 : i4
    }
}
