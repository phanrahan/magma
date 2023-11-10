module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_lazy_array_resolve(in %I: i2, in %S: i1, out O: i2) {
        %0 = hw.constant 1 : i2
        %1 = comb.shru %I, %0 : i2
        %2 = comb.extract %1 from 0 : (i2) -> i1
        %3 = comb.extract %1 from 1 : (i2) -> i1
        %5 = sv.reg : !hw.inout<i2>
        %4 = sv.read_inout %5 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %S {
                %8 = comb.concat %7, %6 : i1, i1
                sv.bpassign %5, %8 : i2
            } else {
                %9 = comb.concat %3, %2 : i1, i1
                sv.bpassign %5, %9 : i2
            }
        }
        %6 = comb.extract %I from 0 : (i2) -> i1
        %7 = comb.extract %I from 1 : (i2) -> i1
        %10 = comb.extract %4 from 0 : (i2) -> i1
        %12 = sv.wire sym @test_when_lazy_array_resolve._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %12, %10 : i1
        %11 = sv.read_inout %12 : !hw.inout<i1>
        %13 = comb.extract %4 from 1 : (i2) -> i1
        %15 = sv.wire sym @test_when_lazy_array_resolve._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %15, %13 : i1
        %14 = sv.read_inout %15 : !hw.inout<i1>
        %16 = comb.concat %14, %11 : i1, i1
        %17 = comb.extract %I from 0 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %11, %17) : i1, i1, i1
        %18 = comb.extract %I from 1 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %14, %18) : i1, i1, i1
        %20 = hw.constant -1 : i1
        %19 = comb.xor %20, %S : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %11, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %14, %3) : i1, i1, i1
        hw.output %16 : i2
    }
}
