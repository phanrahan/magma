module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_2d_array_assign(in %I: !hw.array<2xi2>, in %S: i1, out O: !hw.array<2xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<2xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2xi2>>
        sv.alwayscomb {
            sv.if %S {
                %6 = hw.array_create %5, %3 : i2
                sv.bpassign %1, %6 : !hw.array<2xi2>
            } else {
                %7 = hw.array_create %3, %5 : i2
                sv.bpassign %1, %7 : !hw.array<2xi2>
            }
        }
        %2 = hw.constant 0 : i1
        %3 = hw.array_get %I[%2] : !hw.array<2xi2>, i1
        %4 = hw.constant 1 : i1
        %5 = hw.array_get %I[%4] : !hw.array<2xi2>, i1
        %8 = hw.array_get %0[%2] : !hw.array<2xi2>, i1
        %10 = sv.wire sym @test_when_2d_array_assign._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i2>
        sv.assign %10, %8 : i2
        %9 = sv.read_inout %10 : !hw.inout<i2>
        %11 = hw.array_get %0[%4] : !hw.array<2xi2>, i1
        %13 = sv.wire sym @test_when_2d_array_assign._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i2>
        sv.assign %13, %11 : i2
        %12 = sv.read_inout %13 : !hw.inout<i2>
        %14 = hw.array_create %12, %9 : i2
        %15 = hw.array_get %I[%2] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %9, %15) : i1, i2, i2
        %16 = hw.array_get %I[%4] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %16) : i1, i2, i2
        %18 = hw.constant -1 : i1
        %17 = comb.xor %18, %S : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%17, %9, %16) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%17, %12, %15) : i1, i2, i2
        hw.output %14 : !hw.array<2xi2>
    }
}
